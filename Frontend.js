        function storeData() {
            const userAddress = document.getElementById("address").value.trim();
            const userDate = document.getElementById("date").value.trim();

            let messageAddress = '';
            let messageDate = '';
            let debugUrl = "http://34.66.120.146:5000/get?addr=" + userAddress + "&date=" + userDate;
            let theUrl = "http://34.66.120.146:5000/get?addr=" + userAddress + "&date=" + userDate;

            if (userAddress) {
                messageAddress += "Address stored: " + userAddress;
            } else {
                messageAddress += "Please enter a valid address. ";
            }

            if (isValidDate(userDate)) {
                messageDate += "Date stored: " + userDate;
                
            } else {
                debugUrl = "Not Valid Date"
                messageDate += "Enter a valid date.";
            }
            
            document.getElementById("resultMessageAddress").innerText = messageAddress;
            document.getElementById("resultMessageDate").innerText = messageDate;
            document.getElementById("debugUrl").innerText = debugUrl;   

            if (isValidDate(userDate)) {    
                var flights = JSON.parse(getFlights(theUrl, true));
                console.log(flights);
                console.log("~~~~~~~~~~~~~~~ WEEEEEEEEEEE ~~~~~~~~~~~~~~")
                var flightResult = parseFlights(flights);
                console.log(flightResult);
            }

            document.getElementById("resultFlights").innerText = flightResult;
        }

        function isValidDate(dateString) {
            // Check if date is in YYYY-MM-DD format
            const regex = /^\d{4}-\d{2}-\d{2}$/;
            if (!dateString.match(regex)) {
                return false;
            }

            // Parse the date parts to check if it's valid
            const parts = dateString.split("-");
            const year = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10);
            const day = parseInt(parts[2], 10);

            // Check the ranges of month and day
            if (year < 1000 || month < 1 || month > 12 || day < 1 || day > 31) {
                return false;
            }

            // Check for valid day range per month
            const monthDays = [31, (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
            return day <= monthDays[month - 1];
        }


        function getFlights(theUrl) {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open("GET", theUrl, false);
            xmlHttp.send(null);
            return xmlHttp.responseText;
        }

        function parseFlights(flights) {
            let string_result = '';
            for (let i = 0; i < 10; i++) {
                string_result += flights["flights"][i]["airline"] + ": " + flights["flights"][i]["origin"] + "-->" + flights["flights"][i]["dest"] 
                +  " " + parseInt(flights["flights"][i]["duration"]) / 60 + " hours " + flights["flights"][i]["duration"] % 60 + " minutes.  Price: " + flights["flights"][i]["price"] + "\n";
                console.log(string_result);
            }
            // Return the results
            return string_result;
        }

        let selectedOption = null;

        function selectOption(option) {
            const fromButton = document.getElementById("fromButton");
            const toButton = document.getElementById("toButton");

            if (option === 'from') {
                selectedOption = 'from';
                toButton.style.backgroundColor = "#333";
                toButton.style.color = "#666";

                fromButton.style.backgroundColor = "#1BFC06"; 
                fromButton.style.color = "#1BFC06";
                
            } else if (option === 'to') {
                selectedOption = 'to';
                fromButton.style.backgroundColor = "#333";
                fromButton.style.color = "#666";

                toButton.style.backgroundColor = "#1BFC06"; 
                toButton.style.color = "#1BFC06";
            
            }

            console.log(`Currently selected: ${selectedOption}`);
        }
