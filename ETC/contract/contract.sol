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
    mapping (string => address) customerNameToAddress;

    function addCustomer(string memory customerName) public {
        require(msg.sender != address(0));
        addressToCustomerName[msg.sender] = customerName;
        customerNameToAddress[customerName] = msg.sender;
    }

    function deleteCustomer() public {
        addressToCustomerName[msg.sender] = '';
    }

    function retrieveName(address customerAddress) public returns (string memory) {
        return addressToCustomerName[customerAddress];
    }

    function retrieveAddress(string memory customerName) public returns (address) {
        return customerNameToAddress[customerName];
    }

    function () external payable {}

    function deleteContract() public ownerOnly {
        selfdestruct(address(owner));
    }
}
