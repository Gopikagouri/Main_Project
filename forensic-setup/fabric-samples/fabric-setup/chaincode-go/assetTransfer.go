/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
	"github.com/hyperledger/fabric-samples/asset-transfer-basic/chaincode-go/chaincode"
)

func main() {
	caseChaincode, err := contractapi.NewChaincode(&chaincode.SmartContract{})
	if err != nil {
		log.Panicf("Error creating case-basic chaincode: %v", err)
	}

	if err := caseChaincode.Start(); err != nil {
		log.Panicf("Error starting case-basic chaincode: %v", err)
	}
}
