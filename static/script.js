async function analyzeWebsite() {

    const website = document.getElementById("websiteInput").value.trim();

    if (!website) {
        alert("Please enter a website URL");
        return;
    }

    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                website: website
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("Backend Error:\n\n" + JSON.stringify(data, null, 2));
            return;
        }

        document.getElementById("purpose").innerText =
            data.purpose || "No data available";

        document.getElementById("competitors").innerText =
            data.competitors || "No data available";

        document.getElementById("strategy").innerText =
            data.strategy || "No data available";

        document.getElementById("result").style.display = "block";

    } catch (error) {

        console.error(error);
        alert("JS Error: " + error.message);

    } finally {

        document.getElementById("loading").style.display = "none";
    }
}