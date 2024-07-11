package web

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/hyperledger/fabric-gateway/pkg/client"
)

// OrgSetup contains organization's config to interact with the network.
type OrgSetup struct {
	OrgName      string
	MSPID        string
	CryptoPath   string
	CertPath     string
	KeyPath      string
	TLSCertPath  string
	PeerEndpoint string
	GatewayPeer  string
	Gateway      client.Gateway
}

type VaccineInfo struct {
	VaccineID              string            `json:"VaccineID"`
	VaccineName            string            `json:"VaccineName"`
	AgeGroup               string            `json:"AgeGroup"`
	ContraIndications      string            `json:"ContraIndications"`
	MethodOfAdministration string            `json:"MethodOfAdministration"`
	VaccineDescription     string            `json:"VaccineDescription"`
	PharmaceuticalForm     string            `json:"PharmaceuticalForm"`
	Precautions            string            `json:"Precautions"`
	ManufacturerId         string            `json:"ManufacturerId"`
	VaccineExpiryDetail    VaccineExpiryInfo `json:"VaccineExpiryDetails"`
	DistributorId          string            `json:"DistributorId"`
	HospitalId             string            `json:"HospitalId"`
	BlockHash              string            `json:"BlockHash"`
}

type ManufacturerInfo struct {
	VaccineId      string `json:"VaccineId"`
	ManufacturerId string `json:"ManufacturerId"`
}

type HospitalInfo struct {
	VaccineId  string `json:"VaccineId"`
	HospitalId string `json:"HospitalId"`
}

type DitributorInfo struct {
	VaccineId     string `json:"VaccineId"`
	DistributorId string `json:"DistributorId"`
}

type VaccineExpiryInfo struct {
	ManufacturingDate string
	ExpiryDate        string
}

type VaccineExpiryDetail struct {
	VaccineId         string `json:"VaccineId"`
	ManufacturingDate string `json:"ManufacturingDate"`
	ExpiryDate        string `json:"ExpiryDate"`
}

func Bootup(setups OrgSetup) {
	log.Println("Server Started")
	r := mux.NewRouter()

	r.HandleFunc("/api/v1/add-vaccine-info", setups.AddVaccineRequest).Methods("POST")
	r.HandleFunc("/api/v1/add-vaccine-expiry-detail", setups.AddExpiryDetailRequest).Methods("POST")
	r.HandleFunc("/api/v1/add-manufacture-detail", setups.AddManufactureDetailRequest).Methods("POST")
	r.HandleFunc("/api/v1/add-distributor-detail", setups.AddDistributorDetailRequest).Methods("POST")
	r.HandleFunc("/api/v1/add-hospital-detail", setups.AddHospitalDetailRequest).Methods("POST")
	r.HandleFunc("/api/v1/get-all-vaccine-details", setups.GetAllVaccineDetailsRequest).Methods("GET")
	r.HandleFunc("/api/v1/get-vaccine-details", setups.GetVaccineDetailsRequest).Methods("POST")

	err := http.ListenAndServe(":8080", r)
	if err != nil {
		log.Printf("Error starting server: %s\n", err)
	}
}

func (setup *OrgSetup) AddVaccineRequest(w http.ResponseWriter, r *http.Request) {
	var req VaccineInfo
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	log.Println(req)
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	AddVaccineInfo(contract, req.VaccineID, req.VaccineName, req.AgeGroup, req.ContraIndications, req.MethodOfAdministration, req.VaccineDescription, req.PharmaceuticalForm, req.Precautions)
	//return response
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", "Vaccine details added to hyperledger: Vaccine Details Committed succesfully")

}

func (setup *OrgSetup) AddExpiryDetailRequest(w http.ResponseWriter, r *http.Request) {
	var req VaccineExpiryDetail
	err := json.NewDecoder(r.Body).Decode(&req)
	fmt.Println("VaccineId in AddExpiryDetailRequest", req.VaccineId)
	fmt.Println("ManufacturingDate  in AddExpiryDetailRequest", req.ManufacturingDate)
	fmt.Println("ExpiryDate in AddExpiryDetailRequest", req.ExpiryDate)
	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	log.Println(req)
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	AddExpiryInfo(contract, req.VaccineId, req.ManufacturingDate, req.ExpiryDate)
	//return response
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", "Vaccine expiry details added to hyperledger: Vaccine Details Committed succesfully")
}

func (setup *OrgSetup) AddManufactureDetailRequest(w http.ResponseWriter, r *http.Request) {
	var req ManufacturerInfo
	err := json.NewDecoder(r.Body).Decode(&req)
	fmt.Println("VaccineId in AddHospitalDetailRequest", req.VaccineId)
	fmt.Println("DistributorId in AddHospitalDetailRequest", req.ManufacturerId)

	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	log.Println(req)
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	fmt.Println("VaccineId",req.VaccineId)
	fmt.Println("ManufacturerId",req.ManufacturerId)
	AddManufacturerInfo(contract, req.VaccineId, req.ManufacturerId)
	//return response
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", "Vaccine manufacturer details added to hyperledger: Vaccine Details Committed succesfully")
	
}

func (setup *OrgSetup) AddHospitalDetailRequest(w http.ResponseWriter, r *http.Request) {
	var req HospitalInfo
	err := json.NewDecoder(r.Body).Decode(&req)
	fmt.Println("VaccineId in AddHospitalDetailRequest", req.VaccineId)
	fmt.Println("DistributorId in AddHospitalDetailRequest", req.HospitalId)
	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	log.Println(req)
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	AddHospitalInfo(contract, req.VaccineId, req.HospitalId)
	//return response
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", "Vaccine hospital details added to hyperledger: Vaccine Details Committed succesfully")

	
}

func (setup *OrgSetup) AddDistributorDetailRequest(w http.ResponseWriter, r *http.Request) {
	var req DitributorInfo
	err := json.NewDecoder(r.Body).Decode(&req)
	fmt.Println("VaccineId in AddDistributorDetailRequest", req.VaccineId)
	fmt.Println("DistributorId in AddDistributorDetailRequest", req.DistributorId)
	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	log.Println(req)
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	AddDistributorInfo(contract, req.VaccineId, req.DistributorId)
	//return response
	w.WriteHeader(http.StatusOK)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", "Vaccine Distributor details added to hyperledger: Vaccine Details Committed succesfully")
	
}

func (setup *OrgSetup) GetAllVaccineDetailsRequest(w http.ResponseWriter, r *http.Request) {
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	result := GetAllVaccineDetails(contract)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", result)
}

func (setup *OrgSetup) GetVaccineDetailsRequest(w http.ResponseWriter, r *http.Request) {
	var req VaccineInfo

	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Error parsing request body", http.StatusBadRequest)
		return
	}
	channelID := "channel3"
	chainCodeName := "vaccine3-contract"
	network := setup.Gateway.GetNetwork(channelID)
	contract := network.GetContract(chainCodeName)
	fmt.Println("Vaccine Details: ", req)
	result := GetVaccineDetails(contract, req.VaccineID)
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, "%s", result)
}

func AddVaccineInfo(contract *client.Contract, vaccineId string, vaccineName string, ageGroup string, contraIndications string, methodOfAdministration string, vaccineDescription string, pharmaceuticalForm string, precautions string) []byte {
	fmt.Printf("\n--> Submit Transaction: AddVaccineInfo, add the given Vaccine info to the chain\n")
	var VaccineInfo = VaccineInfo{
		VaccineID:              vaccineId,
		VaccineName:            vaccineName,
		AgeGroup:               ageGroup,
		ContraIndications:      contraIndications,
		MethodOfAdministration: methodOfAdministration,
		VaccineDescription:     vaccineDescription,
		PharmaceuticalForm:     pharmaceuticalForm,
		Precautions:            precautions,
	}
	fmt.Println("Vaccine Info: ", VaccineInfo)
	result, err := contract.SubmitTransaction("AddVaccine", vaccineId, vaccineName, ageGroup, contraIndications, methodOfAdministration, vaccineDescription, pharmaceuticalForm, precautions)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}
	fmt.Printf("*** Transaction committed successfully\n")
	return result
}

func AddExpiryInfo(contract *client.Contract, vaccineId string, manufacturingDate string, expiryDate string) []byte {
	fmt.Printf("\n--> Submit Transaction: AddExpiryInfo, add the vaccine expiry info to the chain\n")
	result, err := contract.SubmitTransaction("AddVaccineExpiryDetail", vaccineId, manufacturingDate, expiryDate)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}
	fmt.Printf("*** Transaction committed successfully\n")
	return result
}

func AddManufacturerInfo(contract *client.Contract, vaccineId string, manufacturerId string) []byte {
	fmt.Printf("\n--> Submit Transaction: AddManufacturerInfo, add the vaccine manufacturer info to the chain\n")
	result, err := contract.SubmitTransaction("AddManufactureDetail", vaccineId, manufacturerId)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}
	fmt.Printf("*** Transaction committed successfully\n")
	return result
}

func AddHospitalInfo(contract *client.Contract, vaccineId string, hospitalId string) []byte {
	fmt.Printf("\n--> Submit Transaction: AddHospitalInfo, added hospital info to the chain\n")
	result, err := contract.SubmitTransaction("AddHospitalDetail", vaccineId, hospitalId)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}
	fmt.Printf("*** Transaction committed successfully\n")
	return result
}

func AddDistributorInfo(contract *client.Contract, vaccineId string, distributorId string) []byte {
	fmt.Printf("\n--> Submit Transaction: AddDistributorInfo, add the vaccine distributor info to the chain\n")
	result, err := contract.SubmitTransaction("AddDistributorDetail", vaccineId, distributorId)
	if err != nil {
		panic(fmt.Errorf("failed to submit transaction: %w", err))
	}
	fmt.Printf("*** Transaction committed successfully\n")
	return result
}

func GetAllVaccineDetails(contract *client.Contract) []byte {
	fmt.Printf("\n--> Evaluate Transaction: Get the details of all the vaccine details stored in hyperledger fabric\n")
	result, err := contract.EvaluateTransaction("GetAllVaccineDetails")
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	var vaccineInfos []VaccineInfo
	err = json.Unmarshal(result, &vaccineInfos)
	if err != nil {
		panic(fmt.Errorf("failed to unmarshal JSON: %w", err))
	}

	fmt.Printf("*** Result: %s\n", result)
	return result
}

func GetVaccineDetails(contract *client.Contract, vaccineId string) []byte {
	fmt.Printf("\n--> Evaluate Transaction: GetVaccineDetails will return the details of the vaccine belonging to the particular vaccineId\n")
	result, err := contract.EvaluateTransaction("GetVaccineDetails", vaccineId)
	if err != nil {
		panic(fmt.Errorf("failed to evaluate transaction: %w", err))
	}
	var VaccineInfo VaccineInfo
	err = json.Unmarshal(result, &VaccineInfo)
	if err != nil {
		panic(fmt.Errorf("failed to unmarshal JSON: %w", err))
	}
	fmt.Println("Vaccine Details: ", VaccineInfo)
	fmt.Printf("*** Result: %s\n", result)
	return result
}
