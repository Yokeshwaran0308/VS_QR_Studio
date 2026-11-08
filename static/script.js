async function generateQR() {
    const logo = document.getElementById("logo").files[0];

    const data = {
        text: document.getElementById("text").value,
        mode: document.getElementById("mode").value,
        dark: document.getElementById("dark").value,
        light: document.getElementById("light").value,
        size: document.getElementById("size").value,
        logo: null
    };

    if (!data.text) {
        alert("Enter text or URL!");
        return;
    }

    if (data.mode === "brand" && logo) {
        data.logo = await new Promise(resolve => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.readAsDataURL(logo);
        });
    }

    if (data.mode === "brand" && !logo) {
        alert("Please upload a logo!");
        return;
    }

    const response = await fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        alert("QR generation failed!");
        return;
    }

    const image = await response.blob();
    const url = URL.createObjectURL(image);

    document.getElementById("result").innerHTML =
        `<img src="${url}" width="200"><br>
         <a href="${url}" download="VS_QR.png">Download QR</a>`;
}