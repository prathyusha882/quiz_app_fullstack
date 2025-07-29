// This mock file simulates API calls. Replace with real HTTP requests using Fetch or Axios when backend is ready.

const DUMMY_DATA = [
  { id: 1, title: 'Project Alpha', description: 'Development of a new AI model.' },
  { id: 2, title: 'Marketing Campaign Q3', description: 'Launch new digital marketing initiatives.' },
  { id: 3, title: 'Website Redesign', description: 'Revamp the company website UI/UX.' },
  { id: 4, title: 'Internal Tool Development', description: 'Build a custom tool for HR department.' },
];

// Simulated token-based fetch
export const fetchData = (token) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!token) {
        reject(new Error('401 Unauthorized'));
      } else {
        resolve(DUMMY_DATA);
      }
    }, 1000); // Simulated delay
  });
};

export const addData = (newItem, token) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!token) {
        reject(new Error('401 Unauthorized'));
        return;
      }

      const newId = DUMMY_DATA.length > 0 ? Math.max(...DUMMY_DATA.map(d => d.id)) + 1 : 1;
      const addedItem = { ...newItem, id: newId };
      DUMMY_DATA.push(addedItem);
      resolve(addedItem);
    }, 500);
  });
};

export const updateData = (updatedItem, token) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!token) {
        reject(new Error('401 Unauthorized'));
        return;
      }

      const index = DUMMY_DATA.findIndex(item => item.id === updatedItem.id);
      if (index !== -1) {
        DUMMY_DATA[index] = { ...DUMMY_DATA[index], ...updatedItem };
        resolve(DUMMY_DATA[index]);
      } else {
        reject(new Error('Item not found'));
      }
    }, 500);
  });
};

export const deleteData = (id, token) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!token) {
        reject(new Error('401 Unauthorized'));
        return;
      }

      const initialLength = DUMMY_DATA.length;
      const newData = DUMMY_DATA.filter(item => item.id !== id);
      if (newData.length < initialLength) {
        DUMMY_DATA.length = 0;
        DUMMY_DATA.push(...newData);
        resolve({ success: true, id });
      } else {
        reject(new Error('Item not found'));
      }
    }, 500);
  });
};
