pragma solidity ^0.4.25;

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

    address[] addresses;
    bytes32[] names;

    function addCustomer(bytes32 customerName) public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        addresses.push(msg.sender);
        names.push(customerName);
    }

    function deleteCustomer() public {
        require(msg.sender != address(0));
        require(msg.sender == tx.origin);
        address[] memory moveAddresses;
        bytes32[] memory moveNames;
        bool shift = false;
        for (uint i = 0; i < addresses.length; ++i) {
            if (addresses[i] == msg.sender) {
                shift = true;
            }
            else {
                if (shift == false) {
                    moveAddresses[i] = addresses[i];
                    moveNames[i] = names[i];
                }
                else {
                    moveAddresses[i - 1] = addresses[i];
                    moveNames[i - 1] = names[i];
                }
            }
        }
        addresses = moveAddresses;
        names = moveNames;
    }

    function retrieveName(address customerAddress) external view returns (bytes32) {
        for (uint i = 0; i < addresses.length; ++i) {
            if (addresses[i] == customerAddress) {
                return names[i];
            }
        }
    }

    function retrieveAddresses(bytes32 customerName) external view returns (address[]) {
        address[] memory response;
        for (uint i = 0; i < names.length; ++i) {
            if (names[i] == customerName) {
                response[response.length] = addresses[i];
            }
        }
        return response;
    }

    function listAllAddresses() external view returns (address[], bytes32[]) {
        return (addresses, names);
    }

    function isAddressUsed(address customerAddress) external view returns (bool) {
        for (uint i = 0; i < addresses.length; ++i) {
            if (addresses[i] == customerAddress) {
                return true;
            }
        }
        return false;
    }

    function () external payable {}

    function deleteContract() external ownerOnly {
        selfdestruct(address(owner));
    }
}
