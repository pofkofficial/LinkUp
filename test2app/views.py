from django.http import HttpResponse

# Define a simple view that returns an HTML response
def homepage(request):
    # You can render an HTML template here or generate HTML directly
    html_content = "<html><head><title>Welcome to My Website</title></head><body>"
    html_content += "<h1>Welcome to My Website</h1>"
    html_content += "<p>This is a simple example of a Django view.</p>"
    html_content += "</body></html>"
    
    # Create an HTTP response with the HTML content
    response = HttpResponse(html_content)
    
    return response