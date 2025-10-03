"""
Health Check endpoint para Docker y AWS ELB/ALB

Este endpoint verifica:
1. Django está corriendo
2. Base de datos accesible
3. (Opcional) Otros servicios críticos

Docker HEALTHCHECK lo usa para verificar el contenedor
"""

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Health checks no necesitan CSRF
@require_GET
def health_check(request):
    """
    Health check básico
    Retorna 200 si todo está OK
    """
    status = {
        'status': 'healthy',
        'django': 'ok',
    }
    
    # Verificar conexión a base de datos
    try:
        connection.ensure_connection()
        status['database'] = 'ok'
    except Exception as e:
        logger.error(f"Health check DB failed: {e}")
        status['status'] = 'unhealthy'
        status['database'] = 'error'
        return JsonResponse(status, status=503)
    
    return JsonResponse(status, status=200)


@csrf_exempt
@require_GET
def readiness_check(request):
    """
    Readiness check (listo para recibir tráfico)
    Más estricto que health_check
    """
    checks = {
        'status': 'ready',
        'checks': {}
    }
    
    # Check 1: Base de datos
    try:
        connection.ensure_connection()
        checks['checks']['database'] = 'ok'
    except Exception as e:
        logger.error(f"Readiness DB check failed: {e}")
        checks['status'] = 'not_ready'
        checks['checks']['database'] = str(e)
        return JsonResponse(checks, status=503)
    
    # Check 2: Verificar que migraciones están aplicadas
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            checks['status'] = 'not_ready'
            checks['checks']['migrations'] = 'pending'
            return JsonResponse(checks, status=503)
        checks['checks']['migrations'] = 'ok'
    except Exception as e:
        logger.error(f"Readiness migration check failed: {e}")
        checks['checks']['migrations'] = str(e)
    
    return JsonResponse(checks, status=200)


@csrf_exempt
@require_GET
def liveness_check(request):
    """
    Liveness check (proceso está vivo)
    Kubernetes lo usa para decidir si reiniciar el pod
    """
    return JsonResponse({'status': 'alive'}, status=200)