# Facebook-Post-Reply-BOT

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow.svg)
![AWS](https://img.shields.io/badge/AWS-Lambda-orange.svg)

An automated Facebook comment reply system powered by Python, AWS Lambda, and Meta Graph API.

*Authorized for sharing by The Hong Kong Youth Mathematical Challenge (HKYMC)*

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## 🔍 Overview

FacebookPostReplyBOT is a serverless application that automatically responds to comments on Facebook posts. Built with Python and deployed on AWS Lambda, this bot utilizes Meta Graph API to monitor and reply to user interactions on specified Facebook pages or posts.

Perfect for:
- Business pages requiring timely responses
- Event organizations handling frequent inquiries
- Community managers seeking to automate common responses

Script Overview:
- RenewToken.py : A script for renewing Facebook Page Access Token
- AutoReplyBot.py : A script for automatically replying and messaging on Facebook page post comments.

## ✨ Features

- **Automated Monitoring**: Continuously monitors comments on specified Facebook posts
- **Customizable Responses**: Configure different replies based on comment content or user attributes
- **Serverless Architecture**: Runs on AWS Lambda for cost-effective, scalable deployment

## 📋 Requirements

- Python 3.8+
- AWS Account with Lambda access
- Facebook Developer Account
- Page Access Token with appropriate permissions (e.g. read_engagement)

## 🙏 Acknowledgements

Special thanks to The Hong Kong Youth Mathematical Challenge (HKYMC) for authorizing the sharing of this project.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

google-site-verification: google3af918b20da7352d.html
