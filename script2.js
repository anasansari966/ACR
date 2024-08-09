const chatContainersConfig = [
  { id: 'select', title: 'Patient Info + Medical History Retrieval' },
  { id: 'select_case_study', title: 'Case Setup Retrieval' },
  { id: 'insert', title: 'Patient Info + Extension Insert/Update' },
  { id: 'insert_medical_history', title: 'Medical History Insert/Update' },
  { id: 'insert_case_study', title: 'Case Setup Insert/Update' },
  // Add more configurations as needed
];
let columns = 2;
const base_url = 'http://localhost:8000';
const endpoints = {
  select: '/select/medical_history',
  insert: '/insert/patient',
  insert_medical_history: '/insert/medical_history',
  insert_case_study: '/insert/case_study',
  patient: '/patient',
  select_case_study: '/select/case_study',
  insert_case_study: '/insert/case_study',
};
//NO CHANGES BELOW

let chatContainers = {};

let isChatOpen = {};

console.log(isChatOpen);
function createChatContainers(configs, columns) {
  const chatContainersDiv = document.getElementById('chat-containers');
  chatContainersDiv.innerHTML = ''; // Clear existing content

  let rowDiv;
  configs.forEach((config, index) => {
    if (index % columns === 0) {
      rowDiv = document.createElement('div');
      rowDiv.classList.add('row');
      chatContainersDiv.appendChild(rowDiv);
    }

    const colDiv = document.createElement('div');
    colDiv.classList.add('col', 'p-4', 'm-3', 'border-2', 'shadow-lg');
    colDiv.id = `${config.id}-chat-container`;

    colDiv.innerHTML = `
      <div class="chat-window" id="${config.id}-chat-window">
        <div class="chat-title">${config.title}</div>
        <div class="chat-history" id="${config.id}-chat-history"></div>
        <div class="chat-input-container">
          <input
            type="text"
            class="chat-message-input"
            id="${config.id}-chat-message-input"
            placeholder="Type your message here..."
            autocomplete="off" />
          <button class="chat-send-button" id="${config.id}-chat-send-button">Send</button>
        </div>
      </div>
    `;

    rowDiv.appendChild(colDiv);
  });
}
createChatContainers(chatContainersConfig, columns);

const patientSelect = document.querySelector('#patient-id-select');
async function getPatients() {
  const res = await fetch(`${base_url}${endpoints.patient}`);
  const json = await res.json();
  let options = json['response']
    .map(
      (p) =>
        `<option value="${p.patient_id}">
          ${p.patient_id} - ${p.FirstName}
        </option>`
    )
    .join('\n');
  options = `<option value="new patient">New Patient</option> ` + options;
  patientSelect.innerHTML = options;
}
// getPatients();
// Function to create a chat message element
// Function to create a chat message element
function createChatMessage(message, isUser) {
  const chatMessage = document.createElement('div');
  chatMessage.classList.add('chat-message');
  message = message.replace(/\n/g, '<br>');
  chatMessage.innerHTML = message;

  if (isUser) {
    chatMessage.classList.add('user');
  } else {
    chatMessage.classList.add('bot');
  }

  return chatMessage;
}

// Function to create a loading indicator element
function createLoadingIndicator() {
  const loadingIndicator = document.createElement('div');
  loadingIndicator.classList.add('loading-indicator');
  loadingIndicator.innerHTML =
    '<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span><span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>';
  return loadingIndicator;
}

// Function to handle sending a message
async function sendMessage(type) {
  const chatInput = chatContainers[type].input;
  const chatHistory = chatContainers[type].history;
  const sendButton = chatContainers[type].sendButton;
  const userMessage = chatInput.value.trim();

  if (userMessage) {
    const userChatMessage = createChatMessage(userMessage, true);
    chatHistory.appendChild(userChatMessage);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    chatInput.value = ''; // Clear the input field after sending
    sendButton.disabled = true;

    // Show loading indicator
    const loadingIndicator = createLoadingIndicator();
    chatHistory.appendChild(loadingIndicator);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the bottom to make the loader visible

    let selectedPatientId = patientSelect.selectedOptions[0].value;
    let patientIdMessage = 'With context to patient id  ';
    if (selectedPatientId === 'new patient') {
      patientIdMessage = 'New Patient with info ';
    } else {
      patientIdMessage += `  ${selectedPatientId}`;
    }
    let question = ` ${patientIdMessage} : ${userMessage}`;
    const endpoint = endpoints[type];
    const response = await fetch(`${base_url}${endpoint}?question=${question}`);
    const json_response = await response.json();
    const answer = json_response;

    const botChatMessage = createChatMessage(answer, false);

    // Hide loading indicator
    chatHistory.removeChild(loadingIndicator);

    chatHistory.appendChild(botChatMessage);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the bottom to make the bot's response visible
    setTimeout(() => {
      chatHistory.scrollTop = chatHistory.scrollHeight; // Ensure scrolling to the bottom
      sendButton.disabled = false;
    }, 500); // Simulate a delay for the bot response
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  chatContainersConfig.forEach((config) => {
    isChatOpen = { ...isChatOpen, [config.id]: false };
    chatContainers = {
      ...chatContainers,
      [config.id]: {
        history: document.querySelector(`#${config.id}-chat-history`),
        input: document.querySelector(`#${config.id}-chat-message-input`),
        sendButton: document.querySelector(`#${config.id}-chat-send-button`),
      },
    };
  });

  // Event listener for sending a message on button click or Enter key press
  for (const type in chatContainers) {
    chatContainers[type].sendButton.addEventListener('click', () =>
      sendMessage(type)
    );
    chatContainers[type].input.addEventListener('keyup', (event) => {
      if (event.key === 'Enter') {
        sendMessage(type);
      }
    });
  }

  const loadingScreen = document.getElementById('loading-screen');
  const content = document.getElementById('content');
  function showLoadingScreen() {
    loadingScreen.style.display = 'flex';
    content.style.display = 'none';
  }

  function hideLoadingScreen() {
    loadingScreen.style.display = 'none';
    content.style.display = 'block';
  }

  // Show loading screen initially
  showLoadingScreen();

  try {
    // Simulate fetch call
    const response = await getPatients();
    // Hide loading screen after fetch call is complete
    hideLoadingScreen();
  } catch (error) {
    console.error('Error fetching data:', error);
    hideLoadingScreen();
    // Optionally, you can display an error message to the user here
  }
});
