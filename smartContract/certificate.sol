// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateIssuer {

    struct Certificate {
        string studentName;
        string courseName;
        string issueDate;
    }

    mapping(uint256 => Certificate) public certificates;

    event CertificateIssued(uint256 certificateId, string studentName, string courseName, string issueDate);

    function issueCertificate(uint256 certificateId, string memory studentName, string memory courseName, string memory issueDate) public {
        certificates[certificateId] = Certificate(studentName, courseName, issueDate);
        emit CertificateIssued(certificateId, studentName, courseName, issueDate);
    }

    function getCertificate(uint256 certificateId) public view returns (string memory studentName, string memory courseName, string memory issueDate) {
        Certificate memory cert = certificates[certificateId];
        return (cert.studentName, cert.courseName, cert.issueDate);
    }
}
