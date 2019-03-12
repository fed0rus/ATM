pragma solidity >=0.5.0 <0.6.0;

contract Registrar {

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

    struct Payment {
        address from;
        uint to;
        uint value;
        uint time;
    }
    Payment[] payments;

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
        if (AtN[_address] == 0) {
            return 0;
        }
        return AtN[_address];
    }

    function getAddress(uint _pn) external view returns (address) {
        if (NtA[_pn] == address(0)) {
            return address(0);
        }
        return NtA[_pn];
    }

    function sendMoney(uint _pn, uint _value) public {
        require(msg.sender != address(0));
        Payment memory p;
        p.from = address(msg.sender);
        p.to = _pn;
        p.value = _value;
        p.time = now;
        payments.push(p);
    }

    function addRequest(uint _phoneNumber) public {
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

    /* function listAdd() external view returns (address[] memory, uint[] memory) {
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
    } */

    function listPayments(address caller) external view returns (bool[] memory, uint[] memory, uint[] memory, uint[] memory) {
        bool[] memory fromTo; // 1 / 0
        uint[] memory numbers;
        uint[] memory values;
        uint[] memory times;
        uint l = payments.length;
        for (uint i = 0; i < l; ++i) {
            if (payments[i].from == caller) {
                fromTo[fromTo.length] = true;
                numbers[numbers.length] = payments[i].to;
                values[values.length] = payments[i].value;
                times[times.length] = payments[i].time;
            }
            else if (payments[i].to == AtN[caller]) {
                fromTo[fromTo.length] = false;
                numbers[numbers.length] = AtN[payments[i].from];
                values[values.length] = payments[i].value;
                times[times.length] = payments[i].time;
            }
        }
        return (fromTo, numbers, values, times);
    }

    function confirmRequest(address applicant) public {
        require(msg.sender == owner);
        uint status = requests[applicant];
        if (status == 1) {
            uint number = AtN[applicant];
            AtN[applicant] = 0;
            NtA[number] = address(0);
            requests[applicant] = 0;
            emit UnregistrationConfirmed(applicant);

            uint l = log.length;
            address[] memory save;
            bool flag = false;
            for (uint i = 0; i < l; ++i) {
                if (log[i] == applicant) {
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
        else if (status > 1) {
            AtN[applicant] = requests[applicant];
            NtA[requests[applicant]] = applicant;
            requests[applicant] = 0;
            emit RegistrationConfirmed(applicant);

            uint l = log.length;
            address[] memory save;
            bool flag = false;
            for (uint i = 0; i < l; ++i) {
                if (log[i] == applicant) {
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
    }

    function () external payable {}

    function validate() external pure returns(bool) {
        return true;
    }

    function deleteContract() external {
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
