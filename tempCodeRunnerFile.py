_visual = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_visual = depth_visual.astype(np.uint8)
    depth_visual = cv2.applyColorMap(depth_visual, cv2.COLORMAP_MAGMA)