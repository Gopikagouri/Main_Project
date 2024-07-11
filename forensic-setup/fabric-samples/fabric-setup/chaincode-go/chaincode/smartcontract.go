package chaincode

import (
	"encoding/hex"
	"encoding/json"
	"fmt"
	"strconv"

	"golang.org/x/crypto/sha3"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing vaccine supply chain
type SmartContract struct {
	contractapi.Contract
}

type VaccineInfo struct {
	VaccineID              string              `json:"VaccineID"`
	VaccineName            string              `json:"VaccineName"`
	AgeGroup               string              `json:"AgeGroup"`
	ContraIndications      string              `json:"ContraIndications"`
	MethodOfAdministration string              `json:"MethodOfAdministration"`
	VaccineDescription     string              `json:"VaccineDescription"`
	PharmaceuticalForm     string              `json:"PharmaceuticalForm"`
	Precautions            string              `json:"Precautions"`
	ManufacturerId         string              `json:"ManufacturerId"`
	VaccineExpiryDetail    VaccineExpiryDetail `json:"VaccineExpiryDetails"`
	DistributorId          string              `json:"DistributorId"`
	HospitalId             string              `json:"HospitalId"`
	PreviousBlockHash      string              `json:"PreviousBlockHash"`
	BlockHash              string              `json:"BlockHash"`
}

type VaccineExpiryDetail struct {
	ManufacturingDate string
	ExpiryDate        string
}

func createBlockHash(content string) string {

	// Create a new SHA3-256 hasher
	hasher := sha3.New256()

	// Write the content to the hasher
	hasher.Write([]byte(content))

	// Get the finalized hash
	hashBytes := hasher.Sum(nil)

	// Convert the hash to a hexadecimal string
	hashString := hex.EncodeToString(hashBytes)

	// Print the hash
	fmt.Println("SHA3-256 hash:", hashString)

	return hashString
}

func (s *SmartContract) AddVaccine(ctx contractapi.TransactionContextInterface, vaccineId string, vaccineName string, ageGroup string, contraIndications string, methodOfAdministration string, vaccineDescription string, pharmaceuticalForm string, precautions string) error {
	exists, err := s.CheckVaccineExists(ctx, vaccineId)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the vaccine Id %s already exists", vaccineId)
	}
	integerValue, err := strconv.Atoi(vaccineId)
	if err != nil {
		fmt.Println("Error:", err)
		return err
	}
	previousId := strconv.Itoa(integerValue - 1)
	previousExists, err := s.CheckVaccineExists(ctx, previousId)
	if err != nil {
		return err
	}
	var previousBlockHash string
	if previousExists {
		vaccineInfoBytes, err := ctx.GetStub().GetState(previousId)
		if err != nil {
			return fmt.Errorf("failed to read VaccineInfo with ID %s: %v", previousId, err)
		}

		if vaccineInfoBytes == nil {
			return fmt.Errorf("VaccineInfo with ID %s does not exist", previousId)
		}

		// Unmarshal the current state into a struct
		var existingVaccineInfo VaccineInfo
		err = json.Unmarshal(vaccineInfoBytes, &existingVaccineInfo)
		if err != nil {
			return fmt.Errorf("error unmarshalling VaccineInfo JSON: %v", err)
		}
		previousBlockHash = existingVaccineInfo.BlockHash
	}

	//blockHash := createBlockHash(vaccineId + vaccineName + vaccineType + manufacturer)

	vaccineDetails := VaccineInfo{
		VaccineID:              vaccineId,
		VaccineName:            vaccineName,
		AgeGroup:               ageGroup,
		ContraIndications:      contraIndications,
		MethodOfAdministration: methodOfAdministration,
		VaccineDescription:     vaccineDescription,
		PharmaceuticalForm:     pharmaceuticalForm,
		Precautions:            precautions,
		PreviousBlockHash:      previousBlockHash,
	}
	vaccineDetailsJSON, err := json.Marshal(vaccineDetails)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(vaccineId, vaccineDetailsJSON)
}

func (s *SmartContract) AddVaccineExpiryDetail(ctx contractapi.TransactionContextInterface, vaccineID string, manufacturingDate string, expiryDate string) error {
	// Retrieve the current state of the VaccineInfo
	vaccineInfoBytes, err := ctx.GetStub().GetState(vaccineID)
	if err != nil {
		return fmt.Errorf("failed to read VaccineInfo with ID %s: %v", vaccineID, err)
	}

	if vaccineInfoBytes == nil {
		return fmt.Errorf("VaccineInfo with ID %s does not exist", vaccineID)
	}

	// Unmarshal the current state into a struct
	var existingVaccineInfo VaccineInfo
	err = json.Unmarshal(vaccineInfoBytes, &existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error unmarshalling VaccineInfo JSON: %v", err)
	}
	vaccineExpiryInfo := VaccineExpiryDetail{
		ManufacturingDate: manufacturingDate,
		ExpiryDate:        expiryDate,
	}
	existingVaccineInfo.VaccineExpiryDetail = vaccineExpiryInfo
	existingVaccineInfo.BlockHash = createBlockHash(existingVaccineInfo.VaccineID + existingVaccineInfo.AgeGroup + existingVaccineInfo.VaccineName + existingVaccineInfo.ContraIndications + existingVaccineInfo.DistributorId + existingVaccineInfo.HospitalId + existingVaccineInfo.HospitalId + existingVaccineInfo.ManufacturerId + existingVaccineInfo.MethodOfAdministration + existingVaccineInfo.PharmaceuticalForm + existingVaccineInfo.Precautions + existingVaccineInfo.VaccineDescription)
	// Marshal the updated VaccineInfo back to JSON
	updatedVaccineInfoBytes, err := json.Marshal(existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error marshalling updated VaccineInfo: %v", err)
	}

	// Update the VaccineInfo state on the ledger
	err = ctx.GetStub().PutState(vaccineID, updatedVaccineInfoBytes)
	if err != nil {
		return fmt.Errorf("error updating VaccineInfo on the ledger: %v", err)
	}

	return nil
}

func (s *SmartContract) AddManufactureDetail(ctx contractapi.TransactionContextInterface, vaccineID string, manufacturerId string) error {
	// Retrieve the current state of the Vaccine
	vaccineInfoBytes, err := ctx.GetStub().GetState(vaccineID)
	if err != nil {
		return fmt.Errorf("failed to read VaccineInfo with ID %s: %v", vaccineID, err)
	}

	if vaccineInfoBytes == nil {
		return fmt.Errorf("VaccineInfo with ID %s does not exist", vaccineID)
	}

	// Unmarshal the current state into a struct
	var existingVaccineInfo VaccineInfo
	err = json.Unmarshal(vaccineInfoBytes, &existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error unmarshalling VaccineInfo JSON: %v", err)
	}

	existingVaccineInfo.ManufacturerId = manufacturerId

	// Marshal the updated VaccineInfo back to JSON
	updatedVaccineInfoBytes, err := json.Marshal(existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error marshalling updated VaccineInfo: %v", err)
	}

	// Update the VaccineInfo state on the ledger
	err = ctx.GetStub().PutState(vaccineID, updatedVaccineInfoBytes)
	if err != nil {
		return fmt.Errorf("error updating VaccineInfo on the ledger: %v", err)
	}

	return nil
}

func (s *SmartContract) AddHospitalDetail(ctx contractapi.TransactionContextInterface, vaccineID string, hospitalId string) error {
	// Retrieve the current state of the Vaccine
	vaccineInfoBytes, err := ctx.GetStub().GetState(vaccineID)
	if err != nil {
		return fmt.Errorf("failed to read VaccineInfo with ID %s: %v", vaccineID, err)
	}

	if vaccineInfoBytes == nil {
		return fmt.Errorf("VaccineInfo with ID %s does not exist", vaccineID)
	}

	// Unmarshal the current state into a struct
	var existingVaccineInfo VaccineInfo
	err = json.Unmarshal(vaccineInfoBytes, &existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error unmarshalling VaccineInfo JSON: %v", err)
	}

	existingVaccineInfo.HospitalId = hospitalId

	// Marshal the updated VaccineInfo back to JSON
	updatedVaccineInfoBytes, err := json.Marshal(existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error marshalling updated VaccineInfo: %v", err)
	}

	// Update the VaccineInfo state on the ledger
	err = ctx.GetStub().PutState(vaccineID, updatedVaccineInfoBytes)
	if err != nil {
		return fmt.Errorf("error updating VaccineInfo on the ledger: %v", err)
	}

	return nil
}

func (s *SmartContract) AddDistributorDetail(ctx contractapi.TransactionContextInterface, vaccineID string, distributorId string) error {
	// Retrieve the current state of the Vaccine
	vaccineInfoBytes, err := ctx.GetStub().GetState(vaccineID)
	if err != nil {
		return fmt.Errorf("failed to read VaccineInfo with ID %s: %v", vaccineID, err)
	}

	if vaccineInfoBytes == nil {
		return fmt.Errorf("VaccineInfo with ID %s does not exist", vaccineID)
	}

	// Unmarshal the current state into a struct
	var existingVaccineInfo VaccineInfo
	err = json.Unmarshal(vaccineInfoBytes, &existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error unmarshalling VaccineInfo JSON: %v", err)
	}

	existingVaccineInfo.DistributorId = distributorId

	// Marshal the updated VaccineInfo back to JSON
	updatedVaccineInfoBytes, err := json.Marshal(existingVaccineInfo)
	if err != nil {
		return fmt.Errorf("error marshalling updated VaccineInfo: %v", err)
	}

	// Update the VaccineInfo state on the ledger
	err = ctx.GetStub().PutState(vaccineID, updatedVaccineInfoBytes)
	if err != nil {
		return fmt.Errorf("error updating VaccineInfo on the ledger: %v", err)
	}

	return nil
}

// VaccineExists check the ledger whether the vaccine respective to the particular id exists
func (s *SmartContract) CheckVaccineExists(ctx contractapi.TransactionContextInterface, vaccineId string) (bool, error) {
	vaccineDetailsJSON, err := ctx.GetStub().GetState(vaccineId)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return vaccineDetailsJSON != nil, nil
}

// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) GetVaccineDetails(ctx contractapi.TransactionContextInterface, vaccineId string) (*VaccineInfo, error) {
	vaccineDetailsJSON, err := ctx.GetStub().GetState(vaccineId)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if vaccineDetailsJSON == nil {
		return nil, fmt.Errorf("the vaccine details %s does not exist", vaccineId)
	}

	var vaccineDetails VaccineInfo
	err = json.Unmarshal(vaccineDetailsJSON, &vaccineDetails)
	if err != nil {
		return nil, err
	}

	return &vaccineDetails, nil
}

func (s *SmartContract) GetAllVaccineDetails(ctx contractapi.TransactionContextInterface) ([]*VaccineInfo, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var vaccineDetails []*VaccineInfo
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var vaccineDetail VaccineInfo
		err = json.Unmarshal(queryResponse.Value, &vaccineDetail)
		if err != nil {
			return nil, err
		}
		vaccineDetails = append(vaccineDetails, &vaccineDetail)
	}

	return vaccineDetails, nil
}
