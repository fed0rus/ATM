pragma solidity >=0.5.4 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    mapping (address => string) public addressToCustomerName;

    function addCustomer(string customerName) public {
        require(msg.sender != address(0));
        addressToCustomerName[msg.sender] = customerName;
    }

    function deleteCustomer() public {
        require(msg.sender != address(0));
        delete addressToCustomerName[msg.sender];
    }

    function getStorage() external view returns () {
        
    }

    function isAddressUsed(address customerAddress) external view returns (bool) {
        return uint(addressToCustomerName[customerAddress]) != 0;
    }

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
