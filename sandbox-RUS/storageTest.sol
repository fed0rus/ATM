pragma solidity ^0.5.1;

contract Mortal {
    address payable owner;

    constructor() public {
        require(0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69 != address(0));
        owner = 0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69;
    }

    modifier ownerOnly {
        require(msg.sender == owner);
        _;
    }
}

contract Final is Mortal {

    mapping (address => string) testPolygon;
    function retrieveData(address testAddress) public returns (string memory){
        testPolygon[0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69] = "Its my address";
        return testPolygon[testAddress];
    }

    function () external payable {}

    // Add some mortality
    function deleteContract() public ownerOnly {
        selfdestruct(address(owner));
    }
}
// 0x107b1A1bfff3C07B4389876cbA750738c8cb42df - contract address
