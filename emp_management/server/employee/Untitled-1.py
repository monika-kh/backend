
# class EmpSearchAPI(APIView):
#     def get(self, request):

#         client = Elasticsearch("http://localhost:9200", verify_certs=False, http_auth=('elastic', 'KJy_tProiUqrlDE_H7qF'))

#         # Successful response!
#         client.info()
#         username = request.query_params.get('username', '')
#         city = request.query_params.get('city', '')
#         department = request.query_params.get('department', '')
#         technologies = request.query_params.getlist('technologies', [])
#         # client = Elasticsearch()

#         # Create an Elasticsearch search
#         data = Search(index='employee_index')  # Use the name of your Elasticsearch index

#         # data = Search(using=client)
#         # data = data.filter('term', user__username=username)
#         data = data.filter('term', city=city)
#         data = data.filter('term', department=department)
#         # for tech in technologies:
#         #     data = data.filter('term', technologies_familiar_with=tech)

#         # Execute the search
#         response = data.execute()
#         import pdb;pdb.set_trace()

#         # Return filtered results
#         results = [{'username': hit.user__username, 'city': hit.city, 'department': hit.department} for hit in response]
#         return Response(results)
