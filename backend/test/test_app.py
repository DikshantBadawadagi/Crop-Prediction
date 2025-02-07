import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app import app  # Adjust import as needed
import uuid
import datetime

client = TestClient(app)

# Sample IDs and test data
team_id = "2dcf4ec3-8d29-461c-a053-48a0b73d9a2a"
field_id = str(uuid.uuid4())
user_id = "8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c"
today = datetime.datetime.now().strftime('%Y-%m-%d')
crop="wheat"

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Welcome": "Welcome to the TerraByte API",
        "Link to Documentation": "https://documenter.getpostman.com/view/26558432/2sA3Qwaoyd"
    }

# Create a field to test the other routes
def test_create_field():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.createField') as mock_createField:
        mock_createField.return_value = {
            "status": "success",
            "id": f"{field_id}"
        }
        response = client.post("/createField", json={
            "field_id": field_id,
            "field_name": "Stephan Test Field",
            "crop_type": "wheat",
            "field_area": {
                "type": "Polygon",
                "coordinates": [[-24.87074931861521, 27.159573936176287], [-24.870773452610735, 27.160054051589952], [-24.871036512841457, 27.160062098216997], [-24.87101479229413, 27.159563207340227]]
            },
            "team_id": team_id
        })
        assert response.status_code == 200
        assert response.json() == mock_createField.return_value

def test_get_field_info():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getFieldInfo') as mock_getFieldInfo:
        mock_getFieldInfo.return_value = {
            "id": field_id,
            "field_area": [
                [-24.87074931861521, 27.159573936176287],
                [-24.870773452610734, 27.160054051589952],
                [-24.871036512841457, 27.160062098216997],
                [-24.87101479229413, 27.159563207340227]
            ],
            "field_name": "Stephan Test Field",
            "crop_type": "wheat",
            "team_id": team_id,
            "hectare": 0.211313511746061
        }
        response = client.get(f"/getFieldInfo?field_id={field_id}")
        assert response.status_code == 200
        assert response.json()["id"] == field_id
        assert response.json()["field_name"] == "Stephan Test Field"
        assert response.json()["crop_type"] == "wheat"
        assert response.json()["team_id"] == team_id

def test_get_field_data():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getFieldData') as mock_getFieldData:
        response = client.get(f"/getFieldData?field_id={field_id}&input_date={today}")
        assert response.status_code == 200
        # assert any(item['date'] == today for item in response.json())
        # assert any(item['field_id'] == field_id for item in response.json())

def test_get_team_field_data():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamFieldData') as mock_getTeamFieldData:
        mock_getTeamFieldData.return_value = {
            "field_id": field_id,
            "field_name": "Stephan Test Field",
        }
        response = client.get(f"/getTeamFieldData?team_id={team_id}&n=1")
        assert response.status_code == 200

def test_get_team_fields():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamFields') as mock_getUserFields:
        mock_getUserFields.return_value = [{"id": field_id, "field_name": "Stephan Test Field"}]
        response = client.get(f"/getTeamFields?team_id={team_id}")
        data = response.json()
        assert response.status_code == 200
        assert any(item['id'] == field_id for item in data)

def test_add_to_team():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.addToTeam') as mock_addToTeam:
        mock_addToTeam.return_value = {"success": "User added to team"}
        response = client.post("/addToTeam", json={"team_id": team_id, "user_id": user_id})
        assert response.status_code == 200
        assert response.json() == {"success": "User added to team"}

# def test_remove_from_team():
#     with patch('backend.database.supabaseFunctions.supabaseFunctions.removeFromTeam') as mock_removeFromTeam:
#         mock_removeFromTeam.return_value = {"success": "User removed from team"}
#         response = client.get(f"/removeFromTeam?user_id={user_id}")
#         assert response.status_code == 200
#         assert response.json() == {"success": "User removed from team"}

def test_update_roles():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.updateRoles') as mock_updateRoles:
        mock_updateRoles.return_value = {"success": "Roles updated"}
        response = client.post("/updateRoles", json={"user_id": user_id, "roles": ["farm_manager"]})
        assert response.status_code == 200
        assert response.json() == {"success": "Roles updated"}

def test_get_team_id():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamId') as mock_getTeamId:
        mock_getTeamId.return_value = {"team_id": team_id}
        response = client.get(f"/getTeamId?user_id={user_id}")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"team_id": team_id}

def test_update_field():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.updateField') as mock_updateField:
        mock_updateField.return_value = {
            "status": "success",
            "data": {
                "created_at": "2024-08-10T15:52:58.591935+00:00",
                "field_area": [
                    [
                        -24.87074931861521,
                        27.159573936176287
                    ],
                    [
                        -24.870773452610734,
                        27.160054051589952
                    ],
                    [
                        -24.871036512841457,
                        27.160062098216997
                    ],
                    [
                        -24.87101479229413,
                        27.159563207340227
                    ]
                ],
                "field_name": "Stephan Test Field",
                "crop_type": "maize",
                "team_id": team_id,
                "updated_at": "2024-08-10T15:52:58.591935+00:00",
                "hectare": 0.211313511746061,
                "id": field_id
            }
        }
        response = client.put("/updateField", json={
            "field_id": field_id,
            "field_name": "Stephan Test Field",
            "crop_type": "maize",
            "field_area": {
                "type": "Polygon",
                "coordinates": [[-24.87074931861521, 27.159573936176287], [-24.870773452610735, 27.160054051589952], [-24.871036512841457, 27.160062098216997], [-24.87101479229413, 27.159563207340227]]
            },
            "updated_at": "2024-08-10T15:52:58.591935+00:00",
            "team_id": team_id
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["field_name"] == "Stephan Test Field"
        assert response.json()["data"]["crop_type"] == "maize"

# def test_update_entry():
#     with patch('backend.database.supabaseFunctions.supabaseFunctions.updateEntry') as mock_updateEntry:
#         mock_updateEntry.return_value = {
#             "field_id": field_id,
#             "date": today,
#             "summary": "Field is experiencing a mild 10°C evening with calm winds and partly cloudy skies. Humidity is at 53%, so watch for potential dew formation. Visibility is good at 10,000 meters. Enjoy the clear skies, but dress warmly as the real feel is slightly cooler. \n",
#             "tempmax": 20.83,
#             "tempmin": 9.53,
#             "tempdiurnal": 11.3,
#             "tempmean": 15.18,
#             "pressure": 1021,
#             "humidity": 24,
#             "dew_point": -2.66,
#             "wind_speed": 2.89,
#             "wind_deg": 335,
#             "wind_gust": 3.83,
#             "clouds": 0,
#             "pop": 0,
#             "rain": 0,
#             "uvi": 6.34,
#             "gff": 0,
#             "gdd": 5.18,
#             "hdd": 0.470000000000001,
#             "soil_moisture": 0.135528861443601,
#             "soil_temperature": 17.44,
#             "pet": 0.697171939708955,
#             "health": None,
#             "yield": None,
#             "sprayability": 0.38
#         }
#         response = client.put("/updateEntry", json={
#             "field_id": field_id,
#             "date": today,
#             "summary": "Field is experiencing a mild 10°C evening with calm winds and partly cloudy skies. Humidity is at 53%, so watch for potential dew formation. Visibility is good at 10,000 meters. Enjoy the clear skies, but dress warmly as the real feel is slightly cooler. \n",
#             "tempmax": 20.83,
#             "tempmin": 9.53,
#             "tempdiurnal": 11.3,
#             "tempmean": 15.18,
#             "pressure": 1021,
#             "humidity": 24,
#             "dew_point": -2.66,
#             "wind_speed": 2.89,
#             "wind_deg": 335,
#             "wind_gust": 3.83,
#             "clouds": 0,
#             "pop": 0,
#             "rain": 100,
#             "uvi": 6.34,
#             "gff": 0,
#             "gdd": 5.18,
#             "hdd": 0.470000000000001,
#             "soil_moisture": 0.135528861443601,
#             "soil_temperature": 17.44,
#             "pet": 0.697171939708955,
#             "health": None,
#             "yield": None,
#             "sprayability": 0.38
#         })
#         assert response.status_code == 200
#         print(response.json())
#         assert response.json()["status"] == "success"
#         assert response.json()["data"]["field_id"] == field_id
#         assert response.json()["data"]["rain"] == 100

def test_delete_field():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.deleteField') as mock_deleteField:
        mock_deleteField.return_value = {
            "status": "success",
            "data": {
                "created_at": "2024-08-10T15:52:58.591935+00:00",
                "field_area": [
                    [
                        -24.87074931861521,
                        27.159573936176287
                    ],
                    [
                        -24.870773452610734,
                        27.160054051589952
                    ],
                    [
                        -24.871036512841457,
                        27.160062098216997
                    ],
                    [
                        -24.87101479229413,
                        27.159563207340227
                    ]
                ],
                "field_name": "Stephan Test Field",
                "crop_type": "maize",
                "team_id": f"{team_id}",
                "updated_at": "2024-08-10T15:52:58.591935+00:00",
                "hectare": 0.211313511746061,
                "id": f"{field_id}"
            }
        }
        response = client.post("/deleteField", json={"field_id": field_id})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"]["field_name"] == "Stephan Test Field"
        assert response.json()["data"]["crop_type"] == "maize"
        assert response.json()["data"]["id"] == f"{field_id}"

# ! doesnt work yet
# def test_fetch_weather():
#     with patch('backend.supabaseFunctions.supabaseFunctions.fetchWeatherForAllFields') as mock_fetchWeatherForAllFields:
#         mock_fetchWeatherForAllFields.return_value = {"success": "Weather fetched for all fields"}
#         response = client.get("/fetchWeatherForAllFields")
#         assert response.status_code == 200
#         assert response.json() == {"success": "Weather fetched for all fields"}

# ! doesnt work yet
# def test_fetchSummary():
#     with patch('backend.supabaseFunctions.supabaseFunctions.fetchSummary') as mock_fetchSummary:
#     mock_fetchSummary.return_value = {"success": "Summary fetched for all fields"}
#     response = client.get("/fetchSummary")
#     assert response.status_code == 200
#     assert response.json() == {"success": "Summary fetched for all fields"}

def test_fetchSensorData():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.fetchSensorData') as mock_fetchSensorData:
        mock_fetchSensorData.return_value = {"success": "Sensor data fetched"}
        response = client.get("/fetchSensorData")
        assert response.status_code == 200
        assert response.json() == {'success': 'Sensor data fetched successfully'}

def test_updateEntry():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.updateEntry') as mock_updateEntry:
        mock_updateEntry.return_value = {"success": "Entry updated"}
        response = client.put("/updateEntry", json={"field_id": field_id, "date": today})
        assert response.status_code == 200
        assert response.json() == {"success": "Entry updated"}

def test_getPastYieldAvg():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getPastYieldAvg') as mock_getPastYieldAvg:
        mock_getPastYieldAvg.return_value = {"success": "Yield average fetched"}
        response = client.get("/getPastYieldAvg?crop=sunflower")
        assert response.status_code == 200
        assert response.json() == {"success": "Yield average fetched"}

def test_getTeamFieldsData():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamFieldData') as mock_getTeamFieldsData:
        mock_getTeamFieldsData.return_value = {"success": "Team fields data fetched"}
        response = client.get("/getTeamFieldData?team_id=2dcf4ec3-8d29-461c-a053-48a0b73d9a2a&n=200")
        assert response.status_code == 200
        assert response.json() == {"success": "Team fields data fetched"}

def test_removeFromTeam():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.removeFromTeam') as mock_removeFromTeam:
        mock_removeFromTeam.return_value = {"success": "User removed from team"}
        response = client.put("/removeFromTeam?user_id=8e0ac7f0-8df0-4127-9081-1ab99ee6ad4c")
        assert response.status_code == 200
        assert response.json() == {"success": "User removed from team"}

def test_getTeamDetails():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamDetails') as mock_getTeamDetails:
        mock_getTeamDetails.return_value = {"success": "Team details fetched"}
        response = client.get("/getTeamDetails?team_id=2dcf4ec3-8d29-461c-a053-48a0b73d9a2a")
        assert response.status_code == 200
        assert response.json() == {"success": "Team details fetched"}

# #!doesnt work for now
# # def test_train():
# #     with patch('backend.app.API.train') as mock_train:
# #         mock_train.return_value = {"success": "Training started"}
# #         response = client.post("/train", json={"field_id": field_id, "batch": False, "waitForCompletion": False})
# #         assert response.status_code == 200
# #         assert response.json() == {"success": "Training started"}

def test_sendMessage():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.sendMessage') as mock_sendMessage:
        mock_sendMessage.return_value = {"success": "Message sent"}
        response = client.post("/sendMessage", json={"message": "Hello, how's the weather today?"})
        assert response.status_code == 200
        assert response.json() == {"success": "Message sent"}

def test_getTeamMessages():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamMessages') as mock_getTeamMessages:
        mock_getTeamMessages.return_value = {"success": "Messages fetched"}
        response = client.get("/getTeamMessages?team_id=2dcf4ec3-8d29-461c-a053-48a0b73d9a2a")
        assert response.status_code == 200
        assert response.json() == {"success": "Messages fetched"}

# ! doesnt work yet
# def test_updateUser():
#     with patch('backend.database.supabaseFunctions.supabaseFunctions.updateUser') as mock_updateUser:
#         mock_updateUser.return_value = {"success": "User updated"}
#         response = client.put("/updateUser", json={"id": "ac774d3a-921f-4154-b590-5e05831431a1", "full_name": "Xavier Test Reynolds"})
#         assert response.status_code == 200
#         assert response.json() == {"success": "User updated"}

# ! doesnt work yet
# def test_getUser():
#     with patch('backend.database.supabaseFunctions.supabaseFunctions.getUser') as mock_getUser:
#         mock_getUser.return_value = {"success": "User fetched"}
#         response = client.get("/getUser?user_id=ac774d3a-921f-4154-b590-5e05831431a1")
#         assert response.status_code == 200
#         assert response.json() == {"success": "User fetched"}

def test_market():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getMarketData') as mock_market:
        mock_market.return_value = {"success": "Market API called"}
        response = client.get("/market?crop=sunflower")
        assert response.status_code == 200
        assert response.json() == {"success": "Market API called"}

def test_getTeamYield():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.getTeamYield') as mock_getTeamYield:
        mock_getTeamYield.return_value = {"success": "Team yield fetched"}
        response = client.get("/getTeamYield?team_id=2dcf4ec3-8d29-461c-a053-48a0b73d9a2a")
        assert response.status_code == 200
        assert response.json() == {"success": "Team yield fetched"}

def test_getUPSensorData():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.createUpSensorData') as mock_getUPSensorData:
        mock_getUPSensorData.return_value = {"success": "Sensor data fetched"}
        response = client.get("/getUPSensorData?sensor_id=2CF7F12025200009")
        assert response.status_code == 200
        assert response.json() == {"success": "Sensor data fetched"}

def test_addFieldToSensor():
    with patch('backend.database.supabaseFunctions.supabaseFunctions.addFieldToSensor') as mock_addFieldToSensor:
        mock_addFieldToSensor.return_value = {"success": "Field added to sensor"}
        response = client.post("/addFieldToSensor", json={"sensor_id": "2CF7F12025200009", "field_id": field_id})
        assert response.status_code == 200
        assert response.json() == {"success": "Field added to sensor"}

def test_train_batch_wait_for_completion_empty():
    response = client.post("/train", json={})
    assert response.status_code == 200
    assert response.json() == {'error': 'Field ID is required or `batch` must be set to `true`'}

# def test_train_batch_wait_for_completion():
#     response = client.post("/train", json={"batch": True})
#     assert response.status_code == 200
#     assert response.json() == {'status': 'All models trained successfully'}