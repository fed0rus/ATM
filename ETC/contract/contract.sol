pragma solidity ^0.4.24;

contract Mortal {
    address owner;

    constructor() public {
        require(0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69 != address(0));
        owner = 0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69;
    }

    modifier ownerOnly {
        require(msg.sender == owner);
        _;
    }
}

contract KYC is Mortal {

    mapping (bytes32 => bytes32) public addressToCustomerName;
    mapping (bytes32 => bytes32[]) public customerNameToAddress;
    mapping (bytes32 => bool) public isUsed;
    bytes32[] public everAddress;
    bytes32[] private response;

    function addCustomer(bytes32 customerName) public {
        bytes32 messageSender = bytes32(msg.sender);
        bytes32 txOrigin = bytes32(tx.origin);
        require(uint(messageSender) != 0);
        require(messageSender == txOrigin);
        addressToCustomerName[messageSender] = customerName;
        customerNameToAddress[customerName].push(messageSender);
        everAddress.push(messageSender);
    }

    function deleteCustomer() public {
        bytes32 messageSender = bytes32(msg.sender);
        bytes32 txOrigin = bytes32(tx.origin);
        require(uint(messageSender) != 0);
        require(messageSender == txOrigin);
        bytes32[] memory saved;
        bytes32 name = addressToCustomerName[messageSender];
        addressToCustomerName[messageSender] = bytes32(0);
        bool flag = false;
        uint _length = customerNameToAddress[name].length;
        for (uint i = 0; i < _length; ++i) {
            if (customerNameToAddress[name][i] == messageSender) {
                flag = true;
            }
            else {
                if (flag) {
                    saved[i - 1] = customerNameToAddress[name][i];
                }
                else {
                    saved[i] = customerNameToAddress[name][i];
                }
            }
        }
        customerNameToAddress[name] = saved;
        for (uint j = 0; j < everAddress.length; ++j) {
            if (everAddress[j] == messageSender) {
                everAddress[j] = bytes32(0);
                break;
            }
        }
    }

    function retrieveName(bytes32 customerAddress) external view returns (bytes32) {
        return addressToCustomerName[customerAddress];
    }

    function retrieveAddresses(bytes32 customerName) external view returns (bytes32[]) {
        return customerNameToAddress[customerName];
    }

    function listAllAddresses() external returns (bytes32[]) {
        uint _l = everAddress.length;
        for (uint i = 0; i < _l; ++i) {
            if (uint(everAddress[i]) != 0) {
                response.push(everAddress[i]);
                response.push(addressToCustomerName[everAddress[i]]);
            }
        }
        bytes32[] memory r = response;
        for (uint j = 0; j < 2 * _l; ++j) {
            response[j] = bytes32(0);
        }
        return r;
    }

    function isAddressUsed(bytes32 customerAddress) external view returns (bool) {
        return uint(addressToCustomerName[customerAddress]) != 0;
    }

    function () external payable {}

    function deleteContract() external ownerOnly {
        selfdestruct(address(owner));
    }
}
