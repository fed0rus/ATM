pragma solidity ^0.4.25;

contract Mortal {

    address owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    modifier ownerOnly {
        require(msg.sender == owner);
        _;
    }
}

contract KYC is Mortal {

    mapping (address => bytes32) public addressToCustomerName;
    mapping (bytes32 => address[]) public customerNameToAddress;
    address[] addressLog;

    function addCustomer(bytes32 customerName) public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        addressToCustomerName[msg.sender] = customerName;
        customerNameToAddress[customerName].push(msg.sender);
        addressLog.push(msg.sender);
    }

    function deleteCustomer() public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        address[] memory saved;
        bytes32 name = addressToCustomerName[msg.sender];
        addressToCustomerName[msg.sender] = bytes32(0);
        bool flag = false;
        uint _l = customerNameToAddress[name].length;
        for (uint i = 0; i < _l; ++i) {
            if (customerNameToAddress[name][i] == msg.sender) {
                flag = true;
            }
            else {
                if (flag) {
                    saved[i - 1] = customerNameToAddress[name][i];
                }
                else {
                    saved[i] = customerNameToAddress[name][i];
                }
            }
        }
        customerNameToAddress[name] = saved;
    }

    function retrieveName(address customerAddress) external view returns (bytes32) {
        return addressToCustomerName[customerAddress];
    }

    function retrieveAddresses(bytes32 customerName) external view returns (address[]) {
        return customerNameToAddress[customerName];
    }

    function listAllAddresses() external view returns (address[], bytes32[]) {
        bytes32[] memory names;
        uint _l = addressLog.length;
        for (uint i = 0; i < _l; ++i) {
            names[names.length] = addressToCustomerName[addressLog[i]];
        }
        return (addressLog, names);
    }

    function isAddressUsed(address customerAddress) external view returns (bool) {
        return uint(addressToCustomerName[customerAddress]) != 0;
    }

    function () external payable {}

    function deleteContract() external ownerOnly {
        selfdestruct(address(owner));
    }
}
