import { Storage } from "./storage";
import { STORAGE_KEYS, ROLE_ROOT } from "@/constants";
import { useUserStoreHook } from "@/store/modules/user";
import router from "@/router";

// 负责本地凭证与偏好的读写
export { AuthStorage } from "./token";

/**
 * 权限判断
 */
export function hasPerm(value: string | string[], type: "button" | "role" = "button"): boolean {
  const { roles, perms } = useUserStoreHook().userInfo;

  if (!roles || !perms) {
    return false;
  }

  // 超级管理员拥有所有权限
  if (type === "button" && roles.includes(ROLE_ROOT)) {
    return true;
  }

  const auths = type === "button" ? perms : roles;
  return typeof value === "string"
    ? auths.includes(value)
    : value.some((perm) => auths.includes(perm));
}


