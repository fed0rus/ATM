pragma solidity >=0.5.0 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    event RegistrationRequest(address indexed sender);

    struct addReq {
        bytes10 phoneNumber;
        address customerAddress;
    }

    mapping (bytes10 => address) public NtA; // NtA and AtN stand for "number to address" and vice versa
    mapping (address => bytes10) public AtN;
    addReq[] public addRequests;

    function whoIsOwner() external view returns (address) {
        return owner;
    }

    function changeOwner(address payable newOwner) public {
        require(msg.sender == owner);
        require(newOwner != owner);
        owner = newOwner;
    }

    function getAddressByNumber(bytes10 _number) external view returns (address) {
        return NtA[_number];
    }

    function getNumberByAddress(address _address) external view returns (bytes10) {
        return AtN[_address];
    }

    function addRequest(bytes10 phoneNumber) public {
        require(msg.sender != address(0));
        addReq memory request;
        request.phoneNumber = phoneNumber;
        request.customerAddress = msg.sender;
        addRequests.push(request);
        emit RegistrationRequest(msg.sender);
    }

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
