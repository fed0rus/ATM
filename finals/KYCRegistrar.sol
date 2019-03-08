pragma solidity >=0.5.0 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    event RegistrationRequest(address indexed sender);
    event UnregistrationRequest(address indexed sender);

    mapping (uint => address) public NtA; // NtA and AtN stand for "number to address" and vice versa
    mapping (address => uint) public AtN;

    mapping (address => uint) public addReq;
    mapping (address => bool) public delReq;

    function whoIsOwner() external view returns (address) {
        return owner;
    }

    function changeOwner(address payable newOwner) public {
        require(msg.sender == owner);
        require(newOwner != owner);
        owner = newOwner;
    }

    function getAddressByNumber(uint _number) external view returns (address) {
        return NtA[_number];
    }

    function getNumberByAddress(address _address) external view returns (uint) {
        return AtN[_address];
    }

    function isAddRequestSent(address _address) external view returns (bool) {
        return addReq[_address] != 0;
    }

    function isDelRequestSent(address _address) external view returns (bool) {
        return delReq[_address] == true;
    }

    function addRequest(uint _phoneNumber) public {
        require(msg.sender != address(0));
        require(_phoneNumber >= 10000000000 && _phoneNumber <= 99999999999);
        require(addReq[msg.sender] == 0);
        require(AtN[msg.sender] == 0);
        addReq[msg.sender] = _phoneNumber;
        emit RegistrationRequest(msg.sender);
    }

    function delRequest() public {
        require(msg.sender != address(0));
        require(AtN[msg.sender] != 0);
        delReq[msg.sender] = true;
        emit UnregistrationRequest(msg.sender);
    }

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
