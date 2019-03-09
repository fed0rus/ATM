pragma solidity >=0.5.0 <0.6.0;

contract KYC {

    address payable owner;

    constructor() public {
        require(msg.sender != address(0));
        owner = msg.sender;
    }

    event RegistrationRequest(address indexed sender);
    event UnregistrationRequest(address indexed sender);

    event RegistrationCanceled(address indexed sender);
    event UnregistrationCanceled(address indexed sender);

    event RegistrationConfirmed(address indexed sender);
    event UngistrationConfirmed(address indexed sender);

    mapping (address => uint) public requests;

    /*
        Status codes:
        == 0:
            no requests
        == 1:
            delete request
        > 1:
            add request
    */

    function whoIsOwner() external view returns (address) {
        return owner;
    }

    function changeOwner(address payable newOwner) public {
        require(msg.sender == owner);
        require(newOwner != owner);
        owner = newOwner;
    }

    function getStatus(address _address) external view returns (uint) {
        return requests[_address];
    }

    function addRequest(uint _phoneNumber) public {
        require(msg.sender != address(0));
        require(_phoneNumber >= 10000000000 && _phoneNumber <= 99999999999);
        require(requests[msg.sender] == 0);
        require(AtN[msg.sender] == 0);
        requests[msg.sender] = _phoneNumber;
        emit RegistrationRequest(msg.sender);
    }

    function delRequest() public {
        require(msg.sender != address(0));
        require(requests[msg.sender] == 0)
        require(AtN[msg.sender] != 0);
        requests[msg.sender] = 1;
        emit UnregistrationRequest(msg.sender);
    }

    function cancelRequest() public {
        require(msg.sender != address(0));
        require(requests[msg.sender] != 0);
        bool switch = false;
        if (requests[msg.sender] == 1) {
            switch = true;
        }
        requests[msg.sender] = 0;
        bulkLog.push(msg.sender);
        if (switch) {
            emit UnregistrationCanceled(msg.sender);
        }
        else {
            emit RegistrationCanceled(msg.sender);
        }
    }

    /* function listAdd() external view returns (address[] memory, uint[] memory) {
        uint _bl = bulkLog.length;
        address[] memory addr;
        uint[] memory numb;
        for (uint i = 0; i < _bl; ++i) {
            if (requests[bulkLog[i]] > 1) {
                addr[addr.length] = bulkLog[i];
                numb[numb.length] = requests[bulkLog[i]];
            }
        }
        return (addr, numb);
    }

    function listDel() external view returns (address[] memory, uint[] memory) {
        uint _bl = bulkLog.length;
        address[] memory addr;
        uint[] memory numb;
        for (uint i = 0; i < _bl; ++i) {
            if (requests[bulkLog[i]] == 1) {
                addr[addr.length] = bulkLog[i];
                numb[numb.length] = requests[bulkLog[i]];
            }
        }
        return (addr, numb);
    } */

    function confirmRequest(address applicant) public {
        require(msg.sender == owner);
        uint status = requests[applicant];
        if (status == 1) {
            number = AtN[applicant];
            AtN[applicant] = 0;
            NtA[number] = address(0);
            emit UnegistrationConfirmed(applicant);
        }
        else if (status > 1) {
            AtN[applicant] = requests[applicant];
            NtA[requests[applicant]] = applicant;
            emit RegistrationConfirmed(applicant);
        }
        else {
            revert();
        }
    }

    function () external payable {}

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }

    function watermark() external pure returns (bool) {
        return true;
    }
}
