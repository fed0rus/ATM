pragma solidity >=0.5.0 <0.6.0;

contract PaymentHandler {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    /* stub */

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
