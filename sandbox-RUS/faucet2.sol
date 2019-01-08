pragma solidity ^0.5.2

contract Faucet {
    function withdraw(uint wintdrawAnount) public {
        require(withdrawAmount <= 0.1 ether);
        msg.sender.transfer(withdrawAmount);
    }
    function() public payable {}
}
