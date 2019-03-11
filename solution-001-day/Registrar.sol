pragma solidity ^0.5.2;


contract Registrar {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }
}
