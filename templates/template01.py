ISSUE = '01'
DATE = 'MARCH 25, 2025'
LISTOFTITLES = ''
T1, S1, I1 = '', '', ''
T2, S2, I2 = '', '', ''
T3, S3, I3 = '', '', ''
T4, S4, I4 = '', '', ''
T5, S5, I5 = '', '', ''

CSS = """ * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'BentonSans Book', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .newsletter-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        
        .header {
            padding: 40px;
            border-bottom: 1px solid #eee;
        }
        
        .issue-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .issue-number {
            background: #000;
            color: white;
            padding: 10px 15px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: bold;
        }
        
        .date {
            color: #666;
            font-size: 14px;
        }
        
        .main-title {
            font-size: 62px;
            font-weight: bold;
            line-height: 1.2;
            margin-bottom: 40px;
        }
        
        .hero-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: center;
        }
        
        .hero-content h2 {
            font-size: 32px;
            margin-bottom: 20px;
            line-height: 1.3;
        }
        
        .hero-content p {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.7; 
        }
        
        .hero-image {
            text-align: center;
        }
        
        .hero-image img {
            width: 100%;
            max-width: 400px;
            border-radius: 10px;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
        }
        
        .content-section {
            padding: 40px;
        }
        
        .blue {
            background-color: #2980b9;
            color:white;
        }
        .bluefont {
            color: #2980b9;
        }
        .content-section.blue {
            background-color: #2980b9;
            color: white;
        }
        .update-item.blue {
            background-color: #2980b9;
            color: white;
        }

        
        .author-section {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .author-image {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .author-info h3 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        
        .author-info p {
            color: #666;
            font-size: 14px;
        }
        
        .section-title {
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .section-content p {
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        .updates-section {
            padding: 40px;
            background: white;
        }
        
        .updates-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            margin-top: 30px;
        }
        
        .update-item {
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }
        
        .update-number {
            background: #000;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .update-content img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .update-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .update-text {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .bottom-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
        }
        
        .bottom-left {
            padding: 40px;
            background: #f8f9fa;
        }
        
        .bottom-right {
            padding: 40px;
            background: white;
        }
        
        .feature-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .contact-info {
            background: #f8f9fa;
            padding: 30px;
            margin-top: 30px;
        }
        
        .contact-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            text-align: center;
        }
        
        .contact-item h4 {
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .contact-item p {
            color: #666;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .hero-section,
            .content-grid,
            .updates-grid,
            .bottom-section,
            .contact-grid {
                grid-template-columns: 1fr;
            }
            
            .main-title {
                font-size: 62px;
            }
            
            .hero-content h2 {
                font-size: 24px;
            }
            
            .newsletter-container {
                margin: 10px;
            }
        }
"""
HTMLPROMPT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenAI Weekly | Issue 01</title>
    <style>
       {CSS}
    </style>
</head>
<body>
    <div class="newsletter-container">
        <!-- Header Section -->
        <div class="header">
            <div class="issue-info">
                <div class="issue-number blue">ISSUE {ISSUE}</div>
                <div class="date">{DATE}</div>
            </div>
            
            <h1 class="main-title bluefont">GenAI Weekly</h1>
            
            <div class="hero-section">
                <div class="hero-content">
                    <p>IN THIS ISSUE:</p>
                    <ul style="margin-left: 20px; margin-bottom: 20px;">
                    {LISTOFTITLES}
                    </ul>
                    
                    <h2 class='bluefont'>{T1}</h2>
                    <p>{S1}</p>
                </div>
                
                <div class="hero-image">
                    <img src="{I1}?w=400&h=600&fit=crop" alt="Person working on laptop">
                </div>
            </div>
        </div>
        
        <!-- Content Grid -->
        <div class="content-grid">
                <div class="content-section blue">
                <img src="{I2}" alt="Team meeting" class="feature-image">
                
                <h3 class="section-title">{T2}</h3>
                <p>{S2}</p>
            </div>
            
            <div class="content-section">
                <img src="{I3}" alt="Team meeting" class="feature-image">
                
                <h3 class="section-title">{T3}</h3>
                <p>{S3}</p>
            </div>
        </div>
        
        <!-- Content Grid -->
        <div class="content-grid">
                <div class="content-section">
                <img src="{I4}" alt="Team meeting" class="feature-image">
                
                <h3 class="section-title">{T4}</h3>
                <p>{S4}</p>
            </div>
            
            <div class="content-section blue">
                <img src="{I5}" alt="Team meeting" class="feature-image">
                
                <h3 class="section-title">{T5}</h3>
                <p>{S5}</p>
            </div>
        </div>

        
        <!-- Contact Section -->
        <div class="contact-info">
            <div class="contact-grid">
                <div class="contact-item">
                    <h4>Created with ❤️</h4>
                    
                </div>
                
                <div class="contact-item">
                    <h4>@Johnny's News Express</h4>
                </div>
                
                <div class="contact-item">
           
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""