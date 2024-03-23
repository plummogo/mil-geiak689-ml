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

function hack(text) {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    let decryptedTexts = [];

    for (let shift = 1; shift < alphabet.length; shift++) {
        let decryptedText = text.split('').map(char => {
            if (char.match(/[a-z]/i)) {
                const isUpperCase = char === char.toUpperCase();
                char = char.toLowerCase();
                
                const currentIndex = alphabet.indexOf(char);
                let newIndex = (currentIndex - shift) % 26;
                if (newIndex < 0) newIndex += 26;
                
                char = alphabet[newIndex];
                return isUpperCase ? char.toUpperCase() : char;
            }
            return char;
        }).join('');
        
        decryptedTexts.push(decryptedText);
        console.log(`Shift ${shift}: ${decryptedText}`);
    }

    return decryptedTexts;
}

/*
    // TESZTELÉS
    
    const text = 'szilva';
    const key = 123;

    encrypt(text, key);
    decrypt(ciphertext);
    hack('upcbja');
*/