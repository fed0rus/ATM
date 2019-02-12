pragma solidity ^0.4.24;

contract Mortal {
    address owner;

    constructor() public {
        require(0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69 != address(0));
        owner = 0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69;
    }

    modifier ownerOnly {
        require(msg.sender == owner);
        _;
    }
}

contract KYC is Mortal {

    mapping (address => string) addressToCustomerName;
    mapping (string => address[]) customerNameToAddress;

    function addCustomer(string memory customerName) public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        addressToCustomerName[msg.sender] = customerName;
        customerNameToAddress[customerName].push(msg.sender);
    }

    function deleteCustomer() public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        address[] memory saved;
        string memory name = addressToCustomerName[msg.sender];
        addressToCustomerName[msg.sender] = '';
        bool flag = false;
        uint _length = customerNameToAddress[name].length;
        for (uint i = 0; i < _length; ++i) {
            if (customerNameToAddress[name][i] == msg.sender) {
                flag = true;
            }
            else {
                if (flag){
                    saved[i - 1] = customerNameToAddress[name][i];
                }
                else {
                    saved[i] = customerNameToAddress[name][i];
                }
            }
        }
        customerNameToAddress[name] = saved;
    }

    function retrieveName(address customerAddress) public returns (string memory) {
        return addressToCustomerName[customerAddress];
    }

    function retrieveAddresses(string memory customerName) public returns (address[]) {
        return customerNameToAddress[customerName];
    }

    function listAll() public returns (mapping(string => address)) {
        
    }

    function isAddressUsed(address customerAddress) public returns (bool) {
        return bytes(addressToCustomerName[customerAddress]).length != 0;
    }

    function () external payable {}

    function deleteContract() public ownerOnly {
        selfdestruct(address(owner));
    }
}
