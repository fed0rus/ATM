pragma solidity ^5.0.1;

contract Mortal {
    address owner;

    constructor() public {
        require(OWNERADDRESS != address(0));
        owner = [OWNERADDRESS];
    }

    modifier ownerOnly {
        require(msg.sender == owner);
        _;
    }
}

contract KYC is mortal {

    event Register(indexed address customerAddress, indexed string customerName)
    mapping (address => string) public addressToCustomerName;
    mapping (string => address) public customerNameToAddress

    function registerCustomer(string customerName) public {
        require(name != '', "Please, enter valid name");
        require(msg.sender != address(0));
        require(addressToCustomerName[msg.sender] == false, "You are already registered")
        require(customerNameToAddress[customerName] == false)
        addressToCustomerName[msg.sender] = customerName;
        customerNameToAddress[customerName] = msg.sender;
        emit Register(msg.sender, customerName);
    }

    function deleteCustomer(address customerAddressToDelete) public {
        require(msg.sender == customerAddressToDelete);
        // Delete from DBs
    }

    // Add some mortality
    function deleteContract() public ownerOnly {
        selfdestruct(owner);
    }
}
