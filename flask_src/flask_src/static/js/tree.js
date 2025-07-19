document.addEventListener('DOMContentLoaded', function() {
    // Get the directory structure from the data attribute
    const fileTreeElement = document.getElementById('file-tree');
    const dirStructure = JSON.parse(fileTreeElement.getAttribute('data-dir-structure'));

    // Function to create the HTML for the file tree recursively
    function createTreeHTML(directory) {
        let html = '<ul>';
        directory.forEach(item => {
            const indentStyle = `padding-left: ${item.level * 10}px;`;

            if (item.type === 'folder') {
                html += `<li class="folder" style="${indentStyle}">
                    <button onclick="toggleFolder(this)">${item.name}/</button>
                    <div class="children" style="display: none;">${createTreeHTML(item.children)}</div>
                </li>`;
            } else if (item.type === 'file') {
                html += `<li class="file" style="${indentStyle}" onclick="showFileContent('${item.path}')">${item.name}</li>`;
            }
        });
        html += '</ul>';
        return html;
    }

    // Render the file tree structure in the container
    document.getElementById('tree-container').innerHTML = createTreeHTML(dirStructure);

    // Function to toggle folder visibility
    window.toggleFolder = function(button) {
        const childrenDiv = button.nextElementSibling;
        childrenDiv.style.display = childrenDiv.style.display === 'none' ? 'block' : 'none';
    };

    // Function to fetch and display file content
    window.showFileContent = function(filePath) {
        fetch(`/api/file_content?path=${encodeURIComponent(filePath)}`)
            .then(response => response.json())
            .then(data => {
                const contentDisplay = document.getElementById('content-display');
                if (data.error) {
                    contentDisplay.textContent = "Error: " + data.error;
                } else {
                    contentDisplay.textContent = data.content;
                    Prism.highlightElement(contentDisplay);
                }
            })
            .catch(err => {
                document.getElementById('content-display').textContent = "Error fetching file content.";
            });
    };
});

