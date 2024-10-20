// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthDataStorage {
    address owner;

    // Mapping to store user health data
    mapping(address => string) private healthData;

    // Event to emit when data is stored
    event HealthDataStored(address indexed user, string data);

    constructor() {
        owner = msg.sender;
    }

    // Store health data on blockchain
    function storeHealthData(string memory data) public {
        healthData[msg.sender] = data;
        emit HealthDataStored(msg.sender, data);
    }

    // Retrieve health data
    function getHealthData(address user) public view returns (string memory) {
        return healthData[user];
    }
}
