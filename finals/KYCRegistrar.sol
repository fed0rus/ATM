pragma solidity >=0.5.0 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    mapping (bytes10 => address) public NtA; // NtA and AtN stand for "number to address" and vice versa
    mapping (address => bytes10) public AtN;

    function whoIsOwner() external view returns (address) {
        return owner;
    }

    function changeOwner(address payable newOwner) public {
        require(msg.sender == owner);
        require(newOwner != owner);
        owner = newOwner;
    }

    function getAddressByNumber(bytes10 number) external view returns (address) {
        return NtA[number];
    }

    /* It is assumed that user ??? */

    function addCustomer(bytes10 phoneNumber) public {
        require(msg.sender != address(0));
        NtA[phoneNumber] = msg.sender;
        AtN[msg.sender] = phoneNumber;
    }

    function deleteCustomer() public {
        bytes10 _number = AtN[msg.sender];
        delete AtN[msg.sender];
        delete NtA[_number];
    }

    /* For US-017 */


    /* End */

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
