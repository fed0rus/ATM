pragma solidity ^0.5.1;

contract Faucet {
    function withdraw(uint withdrawAmount) public {
        require(this.balance >= withdrawAmount);
        msg.sender.transfer(withdrawAmount);
    }

    function () public payable {}
}
