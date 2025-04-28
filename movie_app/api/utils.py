def get_serialized_movies(queryset, serializer_class, order_by, context, limit=10):
    """Helper function to serialize movies with pagination and ordering."""
    movies = queryset.order_by(order_by)[:limit]
    return serializer_class(movies, many=True, context=context).data