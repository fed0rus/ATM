pragma solidity >=0.5.4 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    mapping (address => bytes32) public addressToCustomerName;
    address[] addressLog;

    function addCustomer(bytes32 customerName) public {
        require(msg.sender != address(0));
        addressToCustomerName[msg.sender] = customerName;
        addressLog.push(msg.sender);
    }

    function deleteCustomer() public {
        require(msg.sender != address(0));
        delete addressToCustomerName[msg.sender];
    }

    function getStorage() external view returns (address[] memory, bytes32[] memory) {
        uint _l = addressLog.length;
        bytes32[] memory names = new bytes32[](_l);
        for (uint i = 0; i < _l; ++i) {
            names[i] = addressToCustomerName[addressLog[i]];
        }
        return (addressLog, names);
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
