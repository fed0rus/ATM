pragma solidity ^0.5.3;

contract Mortal {
    address payable owner;

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
    event Register(address indexed customerAddress, string indexed customerName);
    mapping (address => string) addressToCustomerName;
    mapping (string => address) customerNameToAddress;

    function registerCustomer(string memory customerName) public {
        require(msg.sender != address(0));
        require(addressToCustomerName[msg.sender] == flag, "You are already registered");
        require(customerNameToAddress[customerName] == flag, "You are already registered");
        addressToCustomerName[msg.sender] = customerName;
        customerNameToAddress[customerName] = msg.sender;
        emit Register(msg.sender, customerName);
    }
    /* function deleteCustomer(address customerAddressToDelete) public {
        require(msg.sender == customerAddressToDelete);
        // Delete from DBs
    }

    function () external payable {}
    // Add some mortality
    function deleteContract() public ownerOnly {
        selfdestruct(address(owner));
    } */
}
