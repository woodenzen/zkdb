function appendToTestMd(links, noteToSearch) {
    const zettelkasten = '/User/will/Dropbox/zettelkasten'; // replace with your directory path
    const noteContent = fs.readFileSync(path.join(zettelkasten, noteToSearch), 'utf8');
    for (let i = 0; i < links.length; i++) {
        const link = links[i];
        if (noteContent.includes(link)) {
            const twelveDigitNumbers = noteContent.match(/\b\d{12}\b/g);
            if (twelveDigitNumbers) {
                console.log(`Found 12-digit numbers in ${noteToSearch}:`, twelveDigitNumbers);
            }
        }
    }
}