pragma solidity >=0.5.0 <0.6.0;

contract KYC {
    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    mapping (address => string) public phonebook;

    function addCustomer(string memory phoneNumber) public {
        require(msg.sender != address(0));
        phonebook[msg.sender] = phoneNumber;
    }

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
