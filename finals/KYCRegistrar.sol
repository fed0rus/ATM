pragma solidity >=0.5.0 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    mapping (string => address) public NtA; // NtA and AtN stand for "number to address" and vice versa
    mapping (address => string) public AtN;

    function whoIsOwner() external returns (address) {
        return owner;
    }

    function changeOwner(address newOwner) public {
        require(msg.sender == owner);
        owner = newOwner;
    }

    /* It is assumed that user ??? */

    function addCustomer(string memory phoneNumber) public {
        require(msg.sender != address(0));
        NtA[phoneNumber] = msg.sender;
        AtN[msg.sender] = phoneNumber;
    }

    function deleteCustomer() public {
        string _number = AtN[msg.sender];
        delete AtN[msg.sender];
        delete NtA[_number];
    }

    /* For US-017 */

    function getAddressByNumber(string memory number) external returns (address) {
        return NtA[number];
    }

    /* End */

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
