pragma solidity >=0.5.0 <0.6.0;

contract Holder {

    constructor() public {
        require(msg.sender != address(0));
    }

    mapping (address => uint) public list;

    function addValidationKYC(address c) public {
        require(msg.sender != address(0));
        require(c != address(0));
        list[c] = 1;
    }

    function addValidationPH(address c) public {
        require(msg.sender != address(0));
        require(c != address(0));
        list[c] = 2;
    }

    function checkValidityKYC(address c) external view returns (bool) {
        return list[c] == 1;
    }

    function checkValidityPH(address c) external view returns (bool) {
        return list[c] == 2;
    }
}
