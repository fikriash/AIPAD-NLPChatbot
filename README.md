# AIPAD: Chatbot AI for Data and Information Requests
![](https://ibb.co/5GdPTMm)

## Overview
In the digital era, AI-powered chatbots based on natural language processing (NLP) have become a popular trend to improve efficiency and user experience. Universitas Padjadjaran (Unpad), focusing on quality and user experience, aims to leverage this technology to enhance efficiency and provide the best service to the academic community and the public.

The AIPAD project: AI Chatbot for Data and Information Requests is proposed to address this need. This chatbot will serve as a virtual assistant that can respond to data and information requests in real-time through the Telegram platform. With advanced NLP technology, the chatbot can understand user text commands, identify keywords, and provide relevant and accurate responses.

Research shows that the implementation of AI-powered chatbots based on NLP can improve the effectiveness and efficiency of services, as well as user experience. Additionally, the Telegram platform has proven to be popular and accepted by the public.

The process of requesting data using a Letter of Request in government agencies is considered inefficient, slow, and difficult. Based on interviews with Unpad's service department, the ticketing system for resolving data and information requests from service users (academic community) is also inefficient.

Therefore, AIPAD is needed to improve the efficiency and quality of the data and information request process in the Unpad environment. By adopting advanced AI-powered chatbot technology based on NLP and limiting the scope of the innovation, it is hoped that the data request process in the workplace will be faster, more efficient, and provide a better user experience.

## Objectives
1. **Build an AI-powered chatbot based on NLP:**
   - Integrate advanced NLP capabilities for natural language understanding.
   - Develop features for responding to data and information requests.

2. **Enhance NLP Service Integration:**
   - Integrate NLP service to enhance language processing capabilities.

3. **Improve Accessibility and Response Speed:**
   - Expand access range and improve chatbot response speed.

4. **Provide Varied Output Formats:**
   - Offer diverse output formats such as excel data, graphs, or text.

5. **Ensure Data Security and Privacy:**
   - Implement appropriate security settings to safeguard user data.

## Technologies Used
- Python
- Telegram-bot
- GPT-4
- SQL

## Features
#### 1. User Registration
- **Description:** This feature is designed to filter access for users affiliated with Universitas Padjadjaran (Unpad) or those outside the university.

#### 2. Data and Information Retrieval
- **Description:** The main feature of AIPAD, allowing users to request data and information. The output can take various forms:
  - **Raw Data (Excel):** Users can request raw data, which will be provided in Excel format.
  - **Aggregate Data (Text):** Users can request aggregated data, and the chatbot will respond with a summary in text format.
  - **Infographics (PNG Chart):** Users can request data visualizations in the form of PNG charts.

#### 3. Enhanced NLP Capabilities
- **Description:** With the integration of the GPT-4 NLP model, the chatbot's chatting capabilities are significantly enhanced, making interactions more flexible and natural.

## Project Structure
```plaintext
.
├── /src
│   ├── /modules
│   │   ├── main.py
│   │   ├── user.py
│   │   └── data_handler.py
│   ├── /templates
│   │   ├── welcome_message.md
│   │   └── data_response.md
│   ├── config.py
│   └── app.py
├── /docs
├── /tests
├── requirements.txt
├── README.md
└── .gitignore

```


## Implementation Result

The implemented chatbot has been successfully utilized by three administrative units within the Universitas Padjadjaran's rectorate. Below are the outcomes of the implementation along with feedback from each unit:

#### 1. Direktorat Perencanaan Sistem Informasi
- **Number of Users:** 3
- **Response and Feedback:**
  - Positive innovation, significantly assisting the Data team in the data integration service process.
- **Suggestions:**
  - Request for a detailed glossary related to terms used in the chatbot, including operational definitions related to data, such as the definition of active students, registered students, calculation of academic years, etc.
  - Feature request to generate queries from natural language input.
  - Suggested using Generative AI for continuous enrichment of the chatbot's knowledge.

#### 2. Direktorat Kemahasiswaan
- **Number of Users:** 2 (Fadhil Hafizh, Dedi Rustandi)
- **Response and Feedback:**
  - Recognized as an efficient breakthrough in data requesting, aiming to minimize differences in data processing across units and faculties.
- **Suggestions:**
  - Request to expand data sources based on the needs of the unit.
  - Example data: graduate data, student achievements, and student activities.

#### 3. Direktorat Riset dan Pengabdian Masyarakat
- **Number of Users:** 3
- **Response and Feedback:**
  - Innovative and significantly helpful in data retrieval; notably quick in obtaining the required data.
- **Suggestions:**
  - Request to add data for program needs, such as for internal research grants. 
  - Suggested adding filters to refine data retrieval, allowing for specific rows or columns.


## Challenges Faced

During the development of this chatbot, several challenges were encountered:

#### 1. Uncertainty in GPT Responses
- **Description:** One notable challenge was the uncertainty in responses generated by GPT as the NLP model. From the initial stages, the responses produced by GPT were not consistently accurate, often yielding different answers for the same question.

#### 2. Finding Comprehensive and Aesthetic Visualization Libraries
- **Description:** The search for a visualization library that is both comprehensive, aesthetically pleasing, and supports the Python programming language posed a challenge. The goal was to find a library that could seamlessly integrate with the chatbot for effective data representation.

#### 3. Response Time from Chat GPT
- **Description:** Another challenge encountered was the extended response time from Chat GPT. The delays in response time affected the overall efficiency of the chatbot, making it crucial to find ways to optimize and streamline the interaction for a more seamless user experience.

These challenges required careful consideration and innovative solutions to ensure the successful implementation and performance of the AIPAD chatbot.



## Future Enhancements

The continuous development of the AIPAD chatbot will proceed through phased stages. Based on the features and identified challenges in AIPAD v.1.0, several developmental steps are planned for the future. The upcoming stages of development include:

1. **Expansion of Data Sources:**
   - Inclusion of data sources covering the core business of Universitas Padjadjaran.

2. **Knowledge Enrichment and Encyclopedia Expansion:**
   - Addition of more extensive knowledge and an enriched encyclopedia within AIPAD.

3. **Diversification of Graph Types in Data Graphics Submenu:**
   - Incorporation of additional types of graphs to provide users with more options for visualizing data.

4. **Direct Query Execution Feature:**
   - Addition of a feature allowing direct execution of queries based on user requests.

5. **Data Request Filtering Feature:**
   - Integration of a feature enabling users to apply filters to data requests for more refined outputs.

6. **Integration with Voice Chat Feature:**
   - Introduction of a feature enabling integration with voice chat, enhancing the chatbot's accessibility and user experience.

These developmental stages aim to address current limitations and enhance AIPAD's capabilities, ensuring it remains a powerful and versatile tool for data and information retrieval.


## Conclusion

AIPAD: NLP-Based AI Chatbot represents a groundbreaking innovation in the realm of data and information request services, streamlining and optimizing the data service processes. The successful release of version 1.0 marks a significant milestone. While the implementation has garnered positive feedback, there are acknowledged areas for improvement, including inconsistent responses, chatbot response delays, and errors in the graph request feature.

Despite these challenges, strategic plans have been outlined to address these weaknesses, and further development is planned post the completion of the ongoing HIKTU research. AIPAD is envisioned to evolve into a more robust and efficient tool, offering enhanced user experiences and contributing significantly to the optimization of data service processes.


## Contributors
- [Fikri Aziz Shalahuddin (Leader)](https://www.linkedin.com/in/fikri-aziz)
- Muhammad Rafli
- Muhammad Fadhil Ardiansyah
</s>


## References
- Rashid, S., Kiyavitskaya, N., & Ratchev, S. (2019). Chatbots for Enhanced Customer Service: Addressing Challenges of Implementation. In Proceedings of the 16th International Conference on e-Business (ICE-B) (pp. 179-186). SCITEPRESS.
- Almeida, R., Araújo, M., & Caseli, H. M. (2020). Designing a Conversational Agent for Student Support in Higher Education. In Proceedings of the 9th Brazilian Conference on Intelligent Systems (BRACIS) (pp. 516-521). ACM.
- Statista. (2023). Most popular global mobile messaging apps as of January 2023, based on number of monthly active users (in millions). Diakses dari https://www.statista.com/statistics/258749/most-popular-global-mobile-messenger-apps/
- Abdullah, R., Abdullah, Z., & Shariff, S. S. M. (2019). An Investigation of Public Sector Employees’ Perception towards Use of Surat Permohonan in Government Agencies. International Journal of Academic Research in Business and Social Sciences, 9(9), 332-340.
- Rahman, A. H. A., Zain, N. I. M., & Haron, H. (2021). The Inefficiency of Data Request Process in Government Agencies: A Case Study of Surat Permohonan. International Journal of Public Administration and Management Research, 7(3), 75-88.

## Profile and Features


| Profile|                      |
|---------------------------------|----------------------|
| Chatbot Name                    | AIPAD                |
| Abbreviation                    | Artificial Intelligence Padjadjaran |
| Version                         | 1.0                  |
| About                           | AI Padjadjaran is an Artificial Intelligence Virtual Assistant specialized in data, possessing knowledge related to Universitas Padjadjaran's core business data and information. |
| Platform                        | Telegram             |
| Features                        | Provides data and information related to the Tridharma of Universitas Padjadjaran in the form of raw data, aggregated data, and graphical data visualization. |
| AIPAD Bot Access Link            | [https://t.me/AIPadjadjaran_bot](https://t.me/AIPadjadjaran_bot) |
| AIPAD Bot Username              | @aipadjadjaran_bot   |
