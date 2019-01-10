pragma solidity ^0.5.1;

contract UTXOBasedToken {

    event Transfer(bytes32 indexed tx_source, bytes32 indexed tx_address, address indexed recipient, uint256 value, uint256 vout);
    address owner;

    struct Transaction {
        address recipient;
        uint256 value;
    }

    uint256 coinbaseSeq = 0;
    mapping (bytes32 => Transaction) utxoPool;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    function transfer(bytes32 _txHash, uint256 _vout, address[] memory _recipients, uint256[] memory _values) public {
        require(_recipients.length == _values.length);
        require(_recipients.length <= 20);
        uint256 total;
        bytes32 db_key = keccak256(abi.encodePacked(_txHash, _vout)); // db_key = hash(nOutputs, txHash)
        require(utxoPool[db_key].recipient == msg.sender); // WTF???
        uint256 utxo_value = utxoPool[db_key].value;

        bytes32 newTxHash = keccak256(abi.encodePacked(_txHash, _vout, _recipients, _values));

        for(uint256 vout=0; vout<_recipients.length; vout++) {
            require(_recipients[vout] != address(0));
            bytes32 new_db_key = keccak256(abi.encodePacked(newTxHash, vout));
            utxoPool[new_db_key] = Transaction(_recipients[vout], _values[vout]);
            require(total < total+_values[vout]);
            total += _values[vout];
            emit Transfer(_txHash, newTxHash, _recipients[vout], _values[vout], vout);
        }

        require(total == utxo_value);
        delete utxoPool[db_key];
    }

    function() external payable {
        require(msg.value > 0);
        bytes32 txHash = keccak256(abi.encodePacked(msg.sender, msg.value, coinbaseSeq));
        bytes32 db_key = keccak256(abi.encodePacked(txHash, uint256(0)));
        utxoPool[db_key] = Transaction(msg.sender, msg.value);
        coinbaseSeq++;
        emit Transfer(bytes32(0), txHash, msg.sender, msg.value, uint256(0));
    }

    function withdraw(uint256 _value) public {
        require(msg.sender == owner);
        require(address(this).balance >= _value);
        msg.sender.transfer(_value);
    }
}
