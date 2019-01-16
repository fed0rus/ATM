pragma solidity ^0.5.1;

import "faucet.sol";

contract Owned {
    address owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
}

contract Mortal is Owned {
    function destroy() public onlyOwner {
        selfdestruct(owner);
    }
}

contract Token is Mortal {
    Faucet supplier;

    constructor() {
        supplier = new Faucet();
        supplier.value(1 ether);
    }

    function destroy() onlyOwner {
        supplier.destroy();
    }
}
