from llama_index.llms import Ollama
import time
import traceback
import httpx

sector_to_sector = ['Food & Restaurants', 'Social & Messaging', 'B2B Services', 'Technology', 'Real Estate', 'SaaS', 'AI Tools', 'Online Gaming', 'Retail & Ecommerce', 'Internet Marketplaces', 'Autos', 'Travel & Entertainment', 'Internet Platforms', 'EdTech', 'Macro', 'FinTech', 'Health & Wellness', 'Media', 'Industrials', 'Other', 'Science & Engineering', 'Crypto', 'Telecom', 'Financials']
sector_to_subsector = {'AI Tools': ['AI Workspace', 'AI Visual & Art', 'AI Writing & Content', 'AI Character & Chat', 'AI HCM', 'AI Natural Language Processing', 'AI Health Care', 'AI Productivity', 'AI Design & Image Generation', 'AI Website Builders', 'AI Data Analytics', 'AI General', 'AI EdTech', 'AI Video Generation', 'AI Customer Support & Experience', 'AI Music Generation', 'AI DevOps & Code Completion', 'AI Legal', 'AI Voice Generation', 'AI Financial'], 'Autos': ['Auto Parts', 'Auto Auctions', 'Auto Repair & Services', 'Manufacturers', 'Auto Finance', 'Dealer Listings', 'DTC', 'Used Car Marketplace'], 'B2B Services': ['Shippers & Trackers', 'IT Services & Consulting', 'Business Intelligence', 'Maintenance & Repair', 'Ad Managers', 'Industrial Distribution', 'Printing & Branding', 'Parts Marketplace', 'Stock Media'], 'Crypto': ['Information', 'Exchanges & Wallets', 'NFT Marketplaces', 'Metaverse & Games', 'Development & Agencies'], 'EdTech': ['Consumer EdTech', 'Online Degrees', 'Classroom EdTech'], 'Financials': ['Exchanges', 'Banking', 'Consumer Finance', 'Investments', 'Financial Data Provider', 'Insurance'], 'FinTech': ['Lending', 'Payments', 'Consumer', 'Retail Investing', 'Merchant Services', 'Insurance'], 'Food & Restaurants': ['Restaurants', 'Specialty Foods', 'Grocery & Meal Kits', 'Food Production', 'Food Brands', 'Food Delivery'], 'Health & Wellness': ['Fitness', 'Online Health'], 'Internet Marketplaces': ['Freelance', 'Vertical Marketplace'], 'Internet Platforms': ['Job Boards', 'Pet Services', 'Dating Sites', 'Consumer Brands', 'Contractor Services', 'Search', 'Personal Finance', 'Sports Gambling', 'Online Casinos', 'Marketing Tools', 'Deals & Promotion'], 'Media': ['Creator Platforms', 'News & Information', 'Streaming', 'Publishers', 'Production', 'Consumer Reviews', 'Sports Media'], 'Online Gaming': ['Online Gaming'], 'Real Estate': ['NonBank Mortgage', 'Storage', 'MLS', 'Real Estate Development', 'Rentals', 'Listings & Showings'], 'Retail & Ecommerce': ['Office Retail', 'Childcare', 'Footwear', 'Online Resale', 'Industrial & Parts', 'Off-Price', 'Travel Retail', 'Electronics Retail', 'Drug Stores', 'Apparel Retail', 'Pet Retail', 'Eyewear', 'Luxury Retail', 'Specialty Retail', 'Dollar Stores', 'Big Box Retail', 'Gifts & Party', 'Home Retail', 'Ecom Marketplace', 'Personal Care', 'Sport & Athleisure', 'Department Stores', 'Sports Equipment', 'Book Stores & Digital Print', 'Beauty & Cosmetics Retail'], 'SaaS': ['Consulting', 'Communication', 'CRM Tools', 'Design & Creative Tools', 'AdTech', 'Commercial Datasets', 'HCM', 'Collaboration', 'IT & DevOps', 'Application Performance Monitoring', 'CyberSecurity', 'Transactional Exchange', 'Data Cloud', 'Digital Distribution', 'Cybersecurity & Network', 'Workstation', 'Cloud Infrastructure', 'Vendor & Expense Management', 'IoT', 'XM', 'SMB SaaS', 'Finance, Legal & Tax', 'Data Integration & Applications', 'IAM', 'Product Hub', 'Mobile Device Management', 'ERP', 'Observability', 'File Sharing', 'Geography & Maps', 'Accounting Software', 'Unified Communications', 'Electronic Design Automation', 'Document Cloud', 'Web Tools', 'Developer Tools', 'Marketing Cloud', 'Domain Hosting'], 'Science & Engineering': ['Chemicals'], 'Social & Messaging': ['Blogs', 'Social Ad Managers', 'Social Media', 'Discussion Forums', 'Messaging'], 'Telecom': ['Cable/Cell Services', 'Telecommunications'], 'Travel & Entertainment': ['Ground Travel', 'Hotels & Accommodation', 'Airlines', 'Water Travel', 'Cruise Lines', 'Entertainment', 'OTA/Metasearch'], 'Macro': ['US Unemployment'], 'Other': ['Tobacco']}
subsector_to_industry = {'Shippers & Trackers': ['Order & Return Trackers', 'Shippers'], 'Consumer EdTech': ['Course Marketplaces', 'Online Curriculums', 'Quizzes & Test Prep', 'Study EdTech', 'Writing Assistance', 'Language EdTech'], 'Insurance': ['Health Insurance', 'Home & Rental Insurance', 'Other Insurance', 'Auto Insurance', 'Life Insurance'], 'Payments': ['Integrated Payment', 'BNPL', 'P2P Payment'], 'Retail Investing': ['Full-service Broker', 'Direct Trading Platforms'], 'Grocery & Meal Kits': ['Grocery Delivery', 'Grocery Stores', 'Meal Kits'], 'Restaurants': ['POS', 'Reservations', 'Restaurant Management'], 'Fitness': ['Home Fitness', 'Sub Gyms', 'On-demand Fitness'], 'Online Health': ['Mental Health', 'Dental Health', 'Eye Care', 'Primary & Chronic Health', 'Pet Health', 'DNA Testing', 'Nutrition', 'Pharmaceutical Brands', 'Dermatology', 'Health Network & Listings', 'Prescriptions & Medicine'], 'Freelance': ['Physical freelance', 'Digital freelance'], 'Streaming': ['Video Streaming', 'Audio Streaming'], 'News & Information': ['Financial News'], 'Office Retail': ['Business Cards & Printing', 'Office Furniture'], 'Home Retail': ['Cleaning Products', 'Furniture', 'Home Security', 'Home Improvement', 'Home Automation', 'Home Furnishings', 'Appliances'], 'Luxury Retail': ['Jewelry'], 'HCM': ['ATS'], 'CRM Tools': ['CRM', 'CSM', 'CRM Suite', 'CXM'], 'SMB SaaS': ['Shop Builders', 'SMB Marketing Tools', 'SMB CRM', 'SMB HCM', 'SMB Finance & Legal', 'SMB Web Builders'], 'Web Tools': ['Web Builders', 'Shop Builders', 'Web Hosting'], 'Airlines': ['Airlines North America', 'Airlines Middle East', 'Airlines Asia', 'Airlines Europe', 'Airlines LATAM', 'Airlines Cargo'], 'Entertainment': ['Movie Theatres', 'Event Ticketing', 'Amusement Parks & Fairs', 'Live Events'], 'Ground Travel': ['Train & Mass', 'Rental Cars'], 'Hotels & Accommodation': ['Alt Accommodation', 'Resorts & Destinations', 'B2B Travel', 'Booking Management', 'Hotel Chains', 'Vacation Clubs'], 'OTA/Metasearch': ['OTA/Meta General', 'OTA/Meta Verticals'], 'US Unemployment': ['UE-SW', 'UE-NE', 'UE-MW', 'UE-SE', 'UE-West']}
industry_to_subindustry = {'Video Streaming': ['Traditional Cable Network', 'Streaming Native'], 'OTA/Meta Verticals': ['OTA/Meta Hotels', 'OTA/Meta Rental Cars']}

def truncate_to_token_limit(content, max_length=4096, average_token_length=1):
    """Truncate content to a maximum token length."""
    # Estimate the max character length based on average token length
    max_char_length = max_length * average_token_length
    return content if len(content) <= max_char_length else content[:max_char_length]

def analyze_website_content_summary(domain, title, meta_description, headings, navigation, main_content, links):
    try:
        print("analyze_website_content", domain)

        combined_content = f"Domain: {domain}\nTitle: {title}\nMeta Description: {meta_description}\nHeadings: {headings}\nNavigation: {navigation}\nMain Content: {main_content}\nLinks: {links}"
        print("combined_content:", combined_content)
        truncated_content = truncate_to_token_limit(combined_content)
        print("truncated_content:", truncated_content)

        llm = Ollama(model="mistral:latest")
        print("LLM initialized")

        prompt = f"What does the website with the following content do? {truncated_content}"
        print("Prompt:", prompt)

        # Adjust timeout and retries
        timeout = 10  # seconds
        retries = 3
        for attempt in range(retries):
            try:
                response = llm.complete(prompt, timeout=timeout)
                print("Response:", response)
                return str(response)
            except httpx.ReadTimeout:
                print(f"Timeout occurred on attempt {attempt + 1}. Retrying...")
                print("Prompt with timeout:", prompt)
                time.sleep(2)
        print("Unable to process given timeouts:", prompt)
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred in analyze_website_content: {e}", domain)
        return None
    
def analyze_website_content_product(domain, title, meta_description, headings, navigation, main_content, links):
    try:
        print("analyze_website_content", domain)

        combined_content = f"Domain: {domain}\nTitle: {title}\nMeta Description: {meta_description}\nHeadings: {headings}\nNavigation: {navigation}\nMain Content: {main_content}\nLinks: {links}"
        print("combined_content:", combined_content)
        truncated_content = truncate_to_token_limit(combined_content)
        print("truncated_content:", truncated_content)

        llm = Ollama(model="mistral:latest")
        print("LLM initialized")

        prompt = f"What is the primary service or product offered by this website given the following content? {truncated_content}"
        print("Prompt:", prompt)

        # Adjust timeout and retries
        timeout = 10  # seconds
        retries = 3
        for attempt in range(retries):
            try:
                # You might need to adjust this part based on how your library handles timeouts
                response = llm.complete(prompt, timeout=timeout)
                print("Response:", response)
                return str(response)
            except httpx.ReadTimeout:
                print(f"Timeout occurred on attempt {attempt + 1}. Retrying...")
                time.sleep(2)  # Wait for 2 seconds before retrying
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred in analyze_website_content: {e}", domain)
        return None

def categorize_website_sector(summary):
    print("categorize_website_sector", summary)
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Create a prompt for MistralAI
        prompt = f"Please categorize this website based on its summary: '{summary}'. The available categories are: {', '.join(sector_to_sector)}."
        print("Prompt:", prompt)  # Log the generated prompt

        # Get the response from MistralAI
        response = llm.complete(prompt)
        print("response & domain", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response_str", response_str)

        # Find the first matching sector in the response
        for sector in sector_to_sector:
            if sector.lower() in response_str.lower():
                return sector

        return f"Sector not found. {str(response)}"
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", summary)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise


def categorize_website_subsector(summary, sector):
    print("categorize_website_subsector", summary)
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Ensure the sector is valid and has subcategories
        if not sector_to_subsector.get(sector):
            return "No subcategories available for this sector"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                f"please determine the subsector of the website. The available subsector in '{sector}' are: {', '.join(sector_to_subsector[sector])}.")
        print("Prompt:", prompt)  # Log the generated prompt

        # Get the response from MistralAI
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response_str", response_str)

        # Find the first matching subcategory in the response
        for subcategory in sector_to_subsector[sector]:
            if subcategory.lower() in response_str.lower():
                return subcategory

        return f"Subsector not found. {str(response)}"
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", sector)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_industry(summary, subsector):
    print("categorize_website_industry", summary)
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Check if the subsector has associated industries
        if not subsector_to_industry.get(subsector):
            return "No industries available for this subsector"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                f"please determine the industry of the website. The available industries in '{subsector}' are: {', '.join(subsector_to_industry[subsector])}.")
        print("Prompt:", prompt)  # Log the generated prompt

        # Get the response from MistralAI
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response_str", response_str)

        # Find the first matching industry in the response
        for industry in subsector_to_industry[subsector]:
            if industry.lower() in response_str.lower():
                return industry

        return f"Industry not found. {str(response)}"
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", subsector)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subindustry(summary, industry):
    print("categorize_website_subindustry", summary)
    try:
        # Initialize MistralAI
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Check if the industry has associated subindustries
        if not industry_to_subindustry.get(industry):
            return "No subindustries available for this industry"

        # Create a prompt for MistralAI
        prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                f"please determine the subindustry of the website. The available subindustries in '{industry}' are: {', '.join(industry_to_subindustry[industry])}.")
        print("Prompt:", prompt)  # Log the generated prompt

        # Get the response from MistralAI
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response_str", response_str)

        # Find the first matching subindustry in the response
        for subindustry in industry_to_subindustry[industry]:
            if subindustry.lower() in response_str.lower():
                return subindustry

        return f"Subindustry not found. {str(response)}"
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", industry)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_sector_w_new_categories(summary):
    print("categorize_website_sector", summary)
    try:
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        prompt = (f"Please categorize this website based on its summary: '{summary}'. "
                f"The available categories are: {', '.join(sector_to_sector)}. "
                f"If none of these fit, please suggest a new appropriate sector. Limit your response to just the sector.")
        print("Prompt:", prompt)  # Log the generated prompt

        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)

        for sector in sector_to_sector:
            if sector.lower() in response_str.lower():
                return sector

        return str(response)
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", summary)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subsector_w_new_categories(summary, sector):
    print("categorize_website_subsector", summary)
    try:
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Check if there are no subsectors available for the sector
        if not sector_to_subsector.get(sector):
            prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                      f"please suggest an appropriate subsector for this website. "
                      "Limit your response to just the subsector name.")
            print("Prompt:", prompt)  # Log the generated prompt
            response = llm.complete(prompt)
            print("response", response)
            return response.text if hasattr(response, 'text') else str(response)

        # When subsectors are available
        prompt = (f"Based on the summary: '{summary}' and its sector '{sector}', "
                  f"please determine the subsector of the website. "
                  f"The available subsectors in '{sector}' are: {', '.join(sector_to_subsector[sector])}. "
                  f"If none of these fit, please suggest a new appropriate subsector. Limit your response to just the subsector.")
        print("Prompt:", prompt)  # Log the generated prompt
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response", response)


        for subcategory in sector_to_subsector[sector]:
            if subcategory.lower() in response_str.lower():
                return subcategory

        return str(response)
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", sector)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise


def categorize_website_industry_w_new_categories(summary, subsector):
    print("categorize_website_industry", summary)
    try:
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Check if there are no industries available for the subsector
        if not subsector_to_industry.get(subsector):
            prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                      f"please suggest an appropriate industry for this website. "
                      "Limit your response to just the industry name.")
            print("Prompt:", prompt)  # Log the generated prompt
            response = llm.complete(prompt)
            print("response", response)
            return response.text if hasattr(response, 'text') else str(response)

        # When industries are available
        prompt = (f"Based on the summary: '{summary}' and its subsector '{subsector}', "
                  f"please determine the industry of the website. "
                  f"The available industries in '{subsector}' are: {', '.join(subsector_to_industry[subsector])}. "
                  f"If none of these fit, please suggest a new appropriate industry. Limit your response to just the industry.")
        print("Prompt:", prompt)  # Log the generated prompt
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response", response)


        for industry in subsector_to_industry[subsector]:
            if industry.lower() in response_str.lower():
                return industry

        return str(response)
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", subsector)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise

def categorize_website_subindustry_w_new_categories(summary, industry):
    print("categorize_website_subindustry", summary)
    try:
        llm = Ollama(model="mistral:latest")
        print("LLM initialized")  # Log LLM initialization

        # Check if there are no subindustries available for the industry
        if not industry_to_subindustry.get(industry):
            prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                      f"please suggest an appropriate subindustry for this website. "
                      "Limit your response to just the subindustry name.")
            print("Prompt:", prompt)  # Log the generated prompt
            response = llm.complete(prompt)
            print("response", response)
            return str(response)

        # When subindustries are available
        prompt = (f"Based on the summary: '{summary}' and its industry '{industry}', "
                  f"please determine the subindustry of the website. "
                  f"The available subindustries in '{industry}' are: {', '.join(industry_to_subindustry[industry])}. "
                  f"If none of these fit, please suggest a new appropriate subindustry. Limit your response to just the subindustry.")
        print("Prompt:", prompt)  # Log the generated prompt
        response = llm.complete(prompt)
        print("response", response)
        # Convert the response to a string (assuming the response text is in the 'text' attribute)
        response_str = response.text if hasattr(response, 'text') else str(response)
        print("response", response)


        for subindustry in industry_to_subindustry[industry]:
            if subindustry.lower() in response_str.lower():
                return subindustry

        return str(response)
    except Exception as e:
        traceback.print_exc()  # Print the full traceback to help diagnose the issue
        print(f"An error occurred: {e}", industry)
        return None
        # Optionally, you can re-raise the exception after catching it
        # raise



