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
    event UnregistrationConfirmed(address indexed sender);

    mapping (address => uint) public AtN;
    mapping (uint => address) public NtA;

    address[] public log;

    mapping (address => uint) public requests;

    /*
        Status codes:
        == 0:
            no requests
        == 1:
            delete request
        > 1:
            add request (status is number)
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

    function getNumber(address _address) external view returns (uint) {
        return AtN[_address];
    }

    function addRequest(uint _phoneNumber) public {
        /* For --del testing */
        /* AtN[0x84F89561c38b380e97aed3F6f8f28263C60925F2] = _phoneNumber; */
        require(msg.sender != address(0));
        require(_phoneNumber >= 10000000000 && _phoneNumber <= 99999999999);
        require(requests[msg.sender] == 0);
        require(AtN[msg.sender] == 0);
        requests[msg.sender] = _phoneNumber;
        emit RegistrationRequest(msg.sender);
        log.push(msg.sender);
    }

    function delRequest() public {
        require(msg.sender != address(0));
        require(requests[msg.sender] == 0);
        require(AtN[msg.sender] != 0);
        requests[msg.sender] = 1;
        emit UnregistrationRequest(msg.sender);
        log.push(msg.sender);
    }

    function cancelRequest() public {
        require(msg.sender != address(0));
        require(requests[msg.sender] != 0);
        bool mutex = false;
        if (requests[msg.sender] == 1) {
            mutex = true;
        }
        requests[msg.sender] = 0;
        if (mutex) {
            emit UnregistrationCanceled(msg.sender);
        }
        else {
            emit RegistrationCanceled(msg.sender);
        }
        uint l = log.length;
        address[] memory save;
        bool flag = false;
        for (uint i = 0; i < l; ++i) {
            if (log[i] == msg.sender) {
                flag = true;
            }
            else {
                if (!flag) {
                    save[i] = log[i];
                }
                else {
                    save[i - 1] = log[i];
                }
            }
        }
        log = save;
    }

    function listAdd() external view returns (address[] memory, uint[] memory) {
        uint l = log.length;
        address[] memory retA;
        uint[] memory retN;
        for (uint i = 0; i < l; ++i) {
            if (requests[log[i]] > 1) {
                retA[retA.length] = log[i];
                retN[retN.length] = requests[log[i]];
            }
        }
        return (retA, retN);
    }

    function listDel() external view returns (address[] memory, uint[] memory) {
        uint l = log.length;
        address[] memory retA;
        uint[] memory retN;
        for (uint i = 0; i < l; ++i) {
            if (requests[log[i]] == 1) {
                retA[retA.length] = log[i];
                retN[retN.length] = AtN[log[i]];
            }
        }
        return (retA, retN);
    }

    function confirmRequest(address applicant) public {
        require(msg.sender == owner);
        uint status = requests[applicant];
        if (status == 1) {
            uint number = AtN[applicant];
            AtN[applicant] = 0;
            NtA[number] = address(0);
            emit UnregistrationConfirmed(applicant);

            uint l = log.length;
            address[] memory save;
            bool flag = false;
            for (uint i = 0; i < l; ++i) {
                if (log[i] == applicant) {
                    flag = true;
                }
                if (!flag) {
                    save[i] = log[i];
                }
                else {
                    save[i - 1] = log[i];
                }
            }
            log = save;
        }
        else if (status > 1) {
            AtN[applicant] = requests[applicant];
            NtA[requests[applicant]] = applicant;
            emit RegistrationConfirmed(applicant);

            uint l = log.length;
            address[] memory save;
            bool flag = false;
            for (uint i = 0; i < l; ++i) {
                if (log[i] == applicant) {
                    flag = true;
                }
                if (!flag) {
                    save[i] = log[i];
                }
                else {
                    save[i - 1] = log[i];
                }
            }
            log = save;
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
}
