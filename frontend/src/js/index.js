document.getElementById('generateBlog').addEventListener('click', async () => {
  const youtubeLink = document.getElementById('youtubeLink').value;
  // console.log({ youtubeLink });

  const blogContent = document.getElementById('blogContent');
  const loadingCircle = document.getElementById('loadingCircle');

  if (youtubeLink) {
    loadingCircle.style.display = 'block';
    blogContent.innerHTML = '';
    const endpointUrl = '/generate-blog';

    try {
      const response = await fetch(endpointUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link: youtubeLink }),
      });
      const data = await response.json();
      // console.log({ data });
      blogContent.innerHTML = data.content;
    } catch (error) {
      console.error('Error occurred:', error);
      alert('Something went wrong. Please try again later.');
    }
    loadingCircle.style.display = 'none';
  } else {
    alert('Please enter a YouTube link.');
  }
});
