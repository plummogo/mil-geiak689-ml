function generateMapping(key) {
    const abc = 'abcdefghijklmnopqrstuvwxyz'.split('');
    const shuffled = abc.slice();

    for (let i = shuffled.length - 1; i > 0; i--) {
        const pseudoRandom = Math.abs((key * i) % shuffled.length);
        [shuffled[i], shuffled[pseudoRandom]] = [shuffled[pseudoRandom], shuffled[i]];
    }

    return abc.reduce((acc, char, index) => {
        acc[char] = shuffled[index];
        return acc;
    }, {});
}

function encrypt(text, key) {
    const charMap = generateMapping(key);
    return text.split('').map(char => charMap[char] || char).join('');
}

function decrypt(text, key) {
    const charMap = generateMapping(key);
    const invCharMap = Object.entries(charMap).reduce((acc, [original, encrypted]) => {
        acc[encrypted] = original;
        return acc;
    }, {});

    return text.split('').map(char => invCharMap[char] || char).join('');
}

/*
    Teszt
    const key = 123;
    const originalText = "hello world";

    const encryptedText = encrypt(originalText, key);
    console.log(`Encrypted: ${encryptedText}`);

    const decryptedText = decrypt(encryptedText, key);
    console.log(`Decrypted: ${decryptedText}`);
*/