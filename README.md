# Youtube Video to Blog Article Generator

## Stack & Tools

<div>
<img src="https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=Django&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Tailwind%20CSS-06B6D4.svg?style=for-the-badge&logo=Tailwind-CSS&logoColor=white" />
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=for-the-badge&logo=OpenAI&logoColor=white" />
<img src="https://img.shields.io/badge/assemblyai-2048cb?style=for-the-badge" />
<img src="https://img.shields.io/badge/aiven-fc4436?style=for-the-badge" />
</div>

## Features

In this app a user can sign up and generate blog articles from Youtube videos simply by entering the video link. AssemblyAI generates a mp3 file from the audio which is then transcripted into text. OpenAI is used to write a blog style article based on the transcript. All generated articles are stored in a PostgreSQL for the user to access them later. The focus of this project was on learning django backend development so the frontend is kept very simple with only html files, some basic javascript & tailwindcss/daisyui for the style.

Idea from [Python Backend Development Course](https://youtu.be/ftKiHCDVwfA?si=9-jNn8F5gm3Wbtcb) by [Code With Tomi](https://www.youtube.com/@CodeWithTomi).

## Preview

<table>
<tbody>

<!--# 1. Reihe  ---------- -->
<tr>

<td align="center">
<img src="./github/ai-blog-preview-1.png"/>
</td>

<td align="center">
<img src="./github/ai-blog-preview-4.png"/>
</td>

</tr>

<!--# 2. Reihe  ---------- -->
<tr>

<td align="center">
<img src="./github/ai-blog-preview-2.png"/>
</td>

<td align="center">
<img src="./github/ai-blog-preview-5.png"/>
</td>
</tr>

<!--# 3. Reihe  ---------- -->
<tr>

<td align="center">
<img src="./github/ai-blog-preview-3.png"/>
</td>

<td align="center">
<img src="./github/ai-blog-preview-6.png"/>
</td>
</tr>

</tbody>
</table>
