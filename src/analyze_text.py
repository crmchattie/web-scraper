from llama_index.llms import Ollama

sector_to_sector = ['Food & Restaurants', 'Social & Messaging', 'B2B Services', 'Technology', 'Real Estate', 'SaaS', 'AI Tools', 'Online Gaming', 'Retail & Ecommerce', 'Internet Marketplaces', 'Autos', 'Travel & Entertainment', 'Internet Platforms', 'EdTech', 'Macro', 'FinTech', 'Health & Wellness', 'Media', 'Industrials', 'Other', 'Science & Engineering', 'Crypto', 'Telecom', 'Financials']
sector_to_subsector = {'AI Tools': ['AI Workspace', 'AI Visual & Art', 'AI Writing & Content', 'AI Character & Chat', 'AI HCM', 'AI Natural Language Processing', 'AI Health Care', 'AI Productivity', 'AI Design & Image Generation', 'AI Website Builders', 'AI Data Analytics', 'AI General', 'AI EdTech', 'AI Video Generation', 'AI Customer Support & Experience', 'AI Music Generation', 'AI DevOps & Code Completion', 'AI Legal', 'AI Voice Generation', 'AI Financial'], 'Autos': ['Auto Parts', 'Auto Auctions', 'Auto Repair & Services', 'Manufacturers', 'Auto Finance', 'Dealer Listings', 'DTC', 'Used Car Marketplace'], 'B2B Services': ['Shippers & Trackers', 'IT Services & Consulting', 'Business Intelligence', 'Maintenance & Repair', 'Ad Managers', 'Industrial Distribution', 'Printing & Branding', 'Parts Marketplace', 'Stock Media'], 'Crypto': ['Information', 'Exchanges & Wallets', 'NFT Marketplaces', 'Metaverse & Games', 'Development & Agencies'], 'EdTech': ['Consumer EdTech', 'Online Degrees', 'Classroom EdTech'], 'Financials': ['Exchanges', 'Banking', 'Consumer Finance', 'Investments', 'Financial Data Provider', 'Insurance'], 'FinTech': ['Lending', 'Payments', 'Consumer', 'Retail Investing', 'Merchant Services', 'Insurance'], 'Food & Restaurants': ['Restaurants', 'Specialty Foods', 'Grocery & Meal Kits', 'Food Production', 'Food Brands', 'Food Delivery'], 'Health & Wellness': ['Fitness', 'Online Health'], 'Internet Marketplaces': ['Freelance', 'Vertical Marketplace'], 'Internet Platforms': ['Job Boards', 'Pet Services', 'Dating Sites', 'Consumer Brands', 'Contractor Services', 'Search', 'Personal Finance', 'Sports Gambling', 'Online Casinos', 'Marketing Tools', 'Deals & Promotion'], 'Media': ['Creator Platforms', 'News & Information', 'Streaming', 'Publishers', 'Production', 'Consumer Reviews', 'Sports Media'], 'Online Gaming': ['Online Gaming'], 'Real Estate': ['NonBank Mortgage', 'Storage', 'MLS', 'Real Estate Development', 'Rentals', 'Listings & Showings'], 'Retail & Ecommerce': ['Office Retail', 'Childcare', 'Footwear', 'Online Resale', 'Industrial & Parts', 'Off-Price', 'Travel Retail', 'Electronics Retail', 'Drug Stores', 'Apparel Retail', 'Pet Retail', 'Eyewear', 'Luxury Retail', 'Specialty Retail', 'Dollar Stores', 'Big Box Retail', 'Gifts & Party', 'Home Retail', 'Ecom Marketplace', 'Personal Care', 'Sport & Athleisure', 'Department Stores', 'Sports Equipment', 'Book Stores & Digital Print', 'Beauty & Cosmetics Retail'], 'SaaS': ['Consulting', 'Communication', 'CRM Tools', 'Design & Creative Tools', 'AdTech', 'Commercial Datasets', 'HCM', 'Collaboration', 'IT & DevOps', 'Application Performance Monitoring', 'CyberSecurity', 'Transactional Exchange', 'Data Cloud', 'Digital Distribution', 'Cybersecurity & Network', 'Workstation', 'Cloud Infrastructure', 'Vendor & Expense Management', 'IoT', 'XM', 'SMB SaaS', 'Finance, Legal & Tax', 'Data Integration & Applications', 'IAM', 'Product Hub', 'Mobile Device Management', 'ERP', 'Observability', 'File Sharing', 'Geography & Maps', 'Accounting Software', 'Unified Communications', 'Electronic Design Automation', 'Document Cloud', 'Web Tools', 'Developer Tools', 'Marketing Cloud', 'Domain Hosting'], 'Science & Engineering': ['Chemicals'], 'Social & Messaging': ['Blogs', 'Social Ad Managers', 'Social Media', 'Discussion Forums', 'Messaging'], 'Telecom': ['Cable/Cell Services', 'Telecommunications'], 'Travel & Entertainment': ['Ground Travel', 'Hotels & Accommodation', 'Airlines', 'Water Travel', 'Cruise Lines', 'Entertainment', 'OTA/Metasearch'], 'Macro': ['US Unemployment'], 'Other': ['Tobacco']}
subsector_to_industry = {'Shippers & Trackers': ['Order & Return Trackers', 'Shippers'], 'Consumer EdTech': ['Course Marketplaces', 'Online Curriculums', 'Quizzes & Test Prep', 'Study EdTech', 'Writing Assistance', 'Language EdTech'], 'Insurance': ['Health Insurance', 'Home & Rental Insurance', 'Other Insurance', 'Auto Insurance', 'Life Insurance'], 'Payments': ['Integrated Payment', 'BNPL', 'P2P Payment'], 'Retail Investing': ['Full-service Broker', 'Direct Trading Platforms'], 'Grocery & Meal Kits': ['Grocery Delivery', 'Grocery Stores', 'Meal Kits'], 'Restaurants': ['POS', 'Reservations', 'Restaurant Management'], 'Fitness': ['Home Fitness', 'Sub Gyms', 'On-demand Fitness'], 'Online Health': ['Mental Health', 'Dental Health', 'Eye Care', 'Primary & Chronic Health', 'Pet Health', 'DNA Testing', 'Nutrition', 'Pharmaceutical Brands', 'Dermatology', 'Health Network & Listings', 'Prescriptions & Medicine'], 'Freelance': ['Physical freelance', 'Digital freelance'], 'Streaming': ['Video Streaming', 'Audio Streaming'], 'News & Information': ['Financial News'], 'Office Retail': ['Business Cards & Printing', 'Office Furniture'], 'Home Retail': ['Cleaning Products', 'Furniture', 'Home Security', 'Home Improvement', 'Home Automation', 'Home Furnishings', 'Appliances'], 'Luxury Retail': ['Jewelry'], 'HCM': ['ATS'], 'CRM Tools': ['CRM', 'CSM', 'CRM Suite', 'CXM'], 'SMB SaaS': ['Shop Builders', 'SMB Marketing Tools', 'SMB CRM', 'SMB HCM', 'SMB Finance & Legal', 'SMB Web Builders'], 'Web Tools': ['Web Builders', 'Shop Builders', 'Web Hosting'], 'Airlines': ['Airlines North America', 'Airlines Middle East', 'Airlines Asia', 'Airlines Europe', 'Airlines LATAM', 'Airlines Cargo'], 'Entertainment': ['Movie Theatres', 'Event Ticketing', 'Amusement Parks & Fairs', 'Live Events'], 'Ground Travel': ['Train & Mass', 'Rental Cars'], 'Hotels & Accommodation': ['Alt Accommodation', 'Resorts & Destinations', 'B2B Travel', 'Booking Management', 'Hotel Chains', 'Vacation Clubs'], 'OTA/Metasearch': ['OTA/Meta General', 'OTA/Meta Verticals'], 'US Unemployment': ['UE-SW', 'UE-NE', 'UE-MW', 'UE-SE', 'UE-West']}
industry_to_subindustry = {'Video Streaming': ['Traditional Cable Network', 'Streaming Native'], 'OTA/Meta Verticals': ['OTA/Meta Hotels', 'OTA/Meta Rental Cars']}

def analyze_website_content(domain, title, meta_description, headings, navigation, main_content):
    print("analyze_website_content")
    # Combine the scraped data into a coherent summary
    combined_content = f"Domain: {domain}\nTitle: {title}\nMeta Description: {meta_description}\nHeadings: {headings}\nNavigation: {navigation}\nMain Content: {main_content}"
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")

        # Create a prompt for MistralAI
        prompt = f"What does the website with the following content do? {combined_content}"

        # Get the response from MistralAI
        response = llm.complete(prompt)
        return response
    except Exception as e:
        print(f"An error occurred in analyze_website_content: {e}")
        return None

def categorize_website_sector(summary):
    print("categorize_website_sector")
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")

        # Create a prompt for MistralAI
        prompt = f"Please categorize this website based on its summary: '{summary}'. The available categories are: {', '.join(sector_to_sector)}."

        # Get the response from MistralAI
        response = llm.complete(prompt)
        response_str = str(response)

        # Find the first matching sector in the response
        for sector in sector_to_sector:
            if sector.lower() in response_str.lower():
                return sector

        return f"Sector not found. {response}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise


def categorize_website_subsector(summary, sector):
    print("categorize_website_subsector")
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")

        # Ensure the sector is valid and has subcategories
        if sector not in sector_to_subsector or not sector_to_subsector[sector]:
            return "No subcategories available for this sector"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                f"please determine the subsector of the website. The available subsector in '{sector}' are: {', '.join(sector_to_subsector[sector])}.")

        # Get the response from MistralAI
        response = llm.complete(prompt)
        response_str = str(response)

        # Find the first matching subcategory in the response
        for subcategory in sector_to_subsector[sector]:
            if subcategory.lower() in response_str.lower():
                return subcategory

        return f"Subsector not found. {response}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_industry(summary, subsector):
    print("categorize_website_industry")
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")

        # Check if the subsector has associated industries
        if subsector not in subsector_to_industry or not subsector_to_industry[subsector]:
            return "No industries available for this subsector"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                f"please determine the industry of the website. The available industries in '{subsector}' are: {', '.join(subsector_to_industry[subsector])}.")

        # Get the response from MistralAI
        response = llm.complete(prompt)
        response_str = str(response)

        # Find the first matching industry in the response
        for industry in subsector_to_industry[subsector]:
            if industry.lower() in response_str.lower():
                return industry

        return f"Industry not found. {response}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subindustry(summary, industry):
    print("categorize_website_subindustry")
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")

        # Check if the industry has associated subindustries
        if industry not in industry_to_subindustry or not industry_to_subindustry[industry]:
            return "No subindustries available for this industry"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                f"please determine the subindustry of the website. The available subindustries in '{industry}' are: {', '.join(industry_to_subindustry[industry])}.")

        # Get the response from MistralAI
        response = llm.complete(prompt)
        response_str = str(response)

        # Find the first matching subindustry in the response
        for subindustry in industry_to_subindustry[industry]:
            if subindustry.lower() in response_str.lower():
                return subindustry

        return f"Subindustry not found. {response}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_sector_w_new_categories(summary):
    print("categorize_website_sector")
    try:
        llm = Ollama(model="mistral:latest")

        prompt = (f"Please categorize this website based on its summary: '{summary}'. "
                f"The available categories are: {', '.join(sector_to_sector)}. "
                f"If none of these fit, please suggest a new appropriate sector. Limit your response to just the sector.")

        response = llm.complete(prompt)
        response_str = str(response)

        for sector in sector_to_sector:
            if sector.lower() in response_str.lower():
                return sector

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subsector_w_new_categories(summary, sector):
    print("categorize_website_subsector")
    try:
        llm = Ollama(model="mistral:latest")

        # Check if there are no subsectors available for the sector
        if sector not in sector_to_subsector or not sector_to_subsector[sector]:
            prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                      f"please suggest an appropriate subsector for this website. "
                      "Limit your response to just the subsector name.")
            response = llm.complete(prompt)
            return str(response)

        # When subsectors are available
        prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                  f"please determine the subsector of the website. "
                  f"The available subsectors in '{sector}' are: {', '.join(sector_to_subsector[sector])}. "
                  f"If none of these fit, please suggest a new appropriate subsector. Limit your response to just the subsector.")
        response = llm.complete(prompt)
        response_str = str(response)

        for subcategory in sector_to_subsector[sector]:
            if subcategory.lower() in response_str.lower():
                return subcategory

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise


def categorize_website_industry_w_new_categories(summary, subsector):
    print("categorize_website_industry")
    try:
        llm = Ollama(model="mistral:latest")

        # Check if there are no industries available for the subsector
        if subsector not in subsector_to_industry or not subsector_to_industry[subsector]:
            prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                      f"please suggest an appropriate industry for this website. "
                      "Limit your response to just the industry name.")
            response = llm.complete(prompt)
            return str(response)

        # When industries are available
        prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                  f"please determine the industry of the website. "
                  f"The available industries in '{subsector}' are: {', '.join(subsector_to_industry[subsector])}. "
                  f"If none of these fit, please suggest a new appropriate industry. Limit your response to just the industry.")
        response = llm.complete(prompt)
        response_str = str(response)

        for industry in subsector_to_industry[subsector]:
            if industry.lower() in response_str.lower():
                return industry

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subindustry_w_new_categories(summary, industry):
    print("categorize_website_subindustry")
    try:
        llm = Ollama(model="mistral:latest")

        # Check if there are no subindustries available for the industry
        if industry not in industry_to_subindustry or not industry_to_subindustry[industry]:
            prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                      f"please suggest an appropriate subindustry for this website. "
                      "Limit your response to just the subindustry name.")
            response = llm.complete(prompt)
            return str(response)

        # When subindustries are available
        prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                  f"please determine the subindustry of the website. "
                  f"The available subindustries in '{industry}' are: {', '.join(industry_to_subindustry[industry])}. "
                  f"If none of these fit, please suggest a new appropriate subindustry. Limit your response to just the subindustry.")
        response = llm.complete(prompt)
        response_str = str(response)

        for subindustry in industry_to_subindustry[industry]:
            if subindustry.lower() in response_str.lower():
                return subindustry

        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise



