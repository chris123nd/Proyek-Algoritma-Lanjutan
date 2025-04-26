// Fungsi untuk memperbarui tampilan grid
function updateGrid(grid, gameOver = false) {
  let gameGrid = document.getElementById("game-grid");
  let gameOverOverlay = document.getElementById("game-over");
  gameGrid.innerHTML = "";

  grid.forEach((row) => {
    row.forEach((value) => {
      let tile = document.createElement("div");
      tile.textContent = value === 0 ? "" : value;
      tile.dataset.value = value;
      gameGrid.appendChild(tile);
    });
  });

  if (gameOver) {
    gameOverOverlay.classList.remove("hidden");
  } else {
    gameOverOverlay.classList.add("hidden");
  }
}

// Inisialisasi state undo
let undoStack = [];

// Mengambil grid dari server
function fetchGrid() {
  fetch("/get_grid")
    .then((response) => response.json())
    .then((grid) => {
      updateGrid(grid);
      window.currentGrid = grid;
      undoStack = [JSON.parse(JSON.stringify(grid))]; // Simpan grid awal
    })
    .catch((error) => console.error("Error:", error));
}

// Fungsi untuk mengirim perintah gerakan ke server
function sendMove(direction) {
  undoStack.push(JSON.parse(JSON.stringify(window.currentGrid))); // Simpan state sebelum gerakan
  fetch("/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grid: window.currentGrid, direction: direction }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateGrid(data.grid, data.game_over);
      window.currentGrid = data.grid;
    })
    .catch((error) => console.error("Error:", error));
}

// Fungsi untuk mereset game
function restartGame() {
  fetch("/reset", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      updateGrid(data.grid);
      window.currentGrid = data.grid;
      undoStack = [JSON.parse(JSON.stringify(data.grid))]; // Reset undo stack
    })
    .catch((error) => console.error("Error:", error));
}

// Fungsi untuk undo
function undoMove() {
  if (undoStack.length > 1) {
    undoStack.pop(); // Kembali ke state sebelumnya
    window.currentGrid = JSON.parse(JSON.stringify(undoStack[undoStack.length - 1]));
    updateGrid(window.currentGrid);
  }
}

// Tangkap input keyboard untuk menggerakkan tiles
document.addEventListener("keydown", function (event) {
  if (event.key === "ArrowLeft") {
    sendMove("left");
  } else if (event.key === "ArrowRight") {
    sendMove("right");
  } else if (event.key === "ArrowUp") {
    sendMove("up");
  } else if (event.key === "ArrowDown") {
    sendMove("down");
  }
});

// Inisialisasi game
window.onload = fetchGrid;
