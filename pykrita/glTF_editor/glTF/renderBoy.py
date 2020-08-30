
import heapq

from . import \
    Scene, Node, Mesh, Camera, Light, Material


def walk_nodes(nodes, depth_frist=True, max_depth=None):
    stack = [(n, 0) for n in nodes]
    while stack:
        node, depth = stack.pop(0 if depth_first else -1)
        yield node, depth
        if depth < max_depth:
            stack[0:0] = ((n, depth + 1) for n in node.children())


def walk_node_ancestors(node):
    cursor = node.parent()
    while cursor:
        yield cursor
        cursor = cursor.parent()


def lights_in_frustum(scene, threshold=0.01, skip_invisible=True):
    """
    solve nearest point in frustum, threshold intensity at point.
    """
    nearestPoint = frustum.nearestPoint(light)
    if light.intensityAtPoint(nearestPoint) >= threshold:
        yield light


def nodes_in_frustum(scene, frustum, skip_invisible=True):
    """
    create Bounding boxes for meshes + manual offset value for skinned?
    """
    yield node


def render(scene, camera):
    # render pre passes
    frustum_lights = list()
    for light in lights_in_frustum(scene, threshold=0.01, skip_invisible=True):
        _render_shadow(light)
        frustum_lights.append(light)
    # render main pass
    trasparents = list()
    for node, z_depth in nodes_in_frustum(scene, camera.frustum, skip_invisible=True):
        if node.is_transparent():
            # sort back to front
            heapq.heappush(trasparents, (z_depth, node))
        else:
            # sort front to back
            # or
            # sort based on render_program before rendering?
            renderNode(node)
    # render transparents in depth order
    for z_depth, node in trasparents:
        renderNode(node)


def renderNode(node):
    # https://github.com/mmatl/pyrender/blob/9ddad1da09582b79a2dd647afc4263899331c128/pyrender/renderer.py#L511
    for light in light_pass(frustum_lights):
        for primitive in mesh.primitives:
            # with bind render program
            # with set uniforms
            # with bind buffers

            # Render mesh
            n_instances = 1
            if primitive.poses is not None:
                n_instances = len(primitive.poses)

            if primitive.indices is not None:
                glDrawElementsInstanced(
                    primitive.mode, primitive.indices.size, GL_UNSIGNED_INT,
                    ctypes.c_void_p(0), n_instances
                )
            else:
                glDrawArraysInstanced(
                    primitive.mode, 0, len(primitive.positions), n_instances
                )
